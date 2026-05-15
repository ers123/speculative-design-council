"""로컬 자료 수집 모듈 — PDF·md·txt → 에이전트 프롬프트 prefix.

설계 원칙:
- 간단함 최우선. 벡터 검색/RAG 없음. 텍스트 prepend만.
- 업로드된 파일은 전부 세션 메모리에만 저장 (디스크 저장 안 함).
- 파일당 상한 + 전체 상한으로 컨텍스트 폭주 방지.

참고: pypdf 추출 패턴은 ../../_working/glance_brief/extract_pdfs.py 의 구조를 따름.
"""

from __future__ import annotations

import io
import os
from typing import List, Dict, Tuple

try:
    import pypdf
    PYPDF_AVAILABLE = True
except ImportError:
    PYPDF_AVAILABLE = False


# 업로드 제약
MAX_FILES = 5
MAX_CHARS_PER_FILE = 8000  # 약 2-3K 토큰
MAX_TOTAL_CHARS = 30000    # 약 7-10K 토큰 (프롬프트 여유 확보)


# ═════════════════════════════════════════════════════════════════════
# 추출기
# ═════════════════════════════════════════════════════════════════════

def extract_text_from_pdf(file_obj, filename: str) -> Tuple[str, str]:
    """Return (text, error). error is empty on success."""
    if not PYPDF_AVAILABLE:
        return "", "pypdf 패키지가 설치되지 않았습니다. requirements.txt 확인."
    try:
        reader = pypdf.PdfReader(file_obj)
        pages = []
        for i, page in enumerate(reader.pages):
            try:
                txt = page.extract_text() or ""
                if txt.strip():
                    pages.append(f"[p.{i+1}] {txt}")
            except Exception as e_page:
                pages.append(f"[p.{i+1} 추출 실패: {e_page}]")
        return "\n".join(pages), ""
    except Exception as e:
        return "", f"PDF 읽기 오류: {e}"


def extract_text_from_txt(file_obj, filename: str) -> Tuple[str, str]:
    try:
        raw = file_obj.read()
        if isinstance(raw, bytes):
            for enc in ("utf-8", "cp949", "euc-kr"):
                try:
                    return raw.decode(enc), ""
                except UnicodeDecodeError:
                    continue
            return raw.decode("utf-8", errors="replace"), "일부 문자 디코딩 실패 (대체 처리)"
        return raw, ""
    except Exception as e:
        return "", f"텍스트 읽기 오류: {e}"


def extract(file_obj, filename: str) -> Tuple[str, str]:
    """Route extraction by file extension. Returns (text, error)."""
    ext = os.path.splitext(filename)[1].lower()
    if ext == ".pdf":
        return extract_text_from_pdf(file_obj, filename)
    if ext in (".md", ".txt"):
        return extract_text_from_txt(file_obj, filename)
    return "", f"지원하지 않는 형식: {ext}"


# ═════════════════════════════════════════════════════════════════════
# 자료 블록 구성
# ═════════════════════════════════════════════════════════════════════

def build_resource_block(resources: List[Dict]) -> str:
    """resources: [{filename, text, ...}] → 프롬프트에 prepend할 블록.

    빈 리스트일 때는 명시적으로 '업로드 자료 없음' 블록을 반환해서
    에이전트가 grounding rule 판정을 할 수 있게 한다.
    """
    if not resources:
        return (
            "=== 업로드 자료 ===\n"
            "(업로드된 자료 없음 — 근거 태깅 시 [추측]만 가능)\n"
            "=== 자료 끝 ===\n\n"
        )

    chunks = ["=== 업로드 자료 ==="]
    total = 0
    for r in resources:
        txt = (r.get("text") or "")[:MAX_CHARS_PER_FILE]
        if total + len(txt) > MAX_TOTAL_CHARS:
            remaining = MAX_TOTAL_CHARS - total
            if remaining <= 0:
                chunks.append(f"\n[이후 파일 {r['filename']} 은 용량 한도로 생략]")
                break
            txt = txt[:remaining]
        chunks.append(f"\n── 파일: {r['filename']} ──\n{txt}")
        total += len(txt)
    chunks.append("\n=== 자료 끝 ===\n")
    return "\n".join(chunks) + "\n"


def resources_manifest(resources: List[Dict]) -> List[Dict]:
    """세션 저장용 경량 매니페스트 (본문 제외)."""
    return [
        {
            "filename": r.get("filename", ""),
            "chars": len(r.get("text") or ""),
            "kind": os.path.splitext(r.get("filename", ""))[1].lower().lstrip("."),
        }
        for r in resources
    ]


# ═════════════════════════════════════════════════════════════════════
# Streamlit uploader 통합 헬퍼 (app.py에서 호출)
# ═════════════════════════════════════════════════════════════════════

def ingest_uploads(uploaded_files) -> Tuple[List[Dict], List[str]]:
    """Streamlit의 st.file_uploader 결과를 받아 자료 리스트와 에러 메시지를 반환."""
    resources: List[Dict] = []
    errors: List[str] = []
    if not uploaded_files:
        return resources, errors

    for uf in uploaded_files[:MAX_FILES]:
        buf = io.BytesIO(uf.getvalue()) if hasattr(uf, "getvalue") else uf
        text, err = extract(buf, uf.name if hasattr(uf, "name") else "unknown")
        if err:
            errors.append(f"{getattr(uf, 'name', 'file')}: {err}")
            if not text:
                continue
        resources.append({
            "filename": getattr(uf, "name", "unknown"),
            "text": text,
        })

    if uploaded_files and len(uploaded_files) > MAX_FILES:
        errors.append(f"파일이 {MAX_FILES}개를 초과하여 앞의 {MAX_FILES}개만 사용합니다.")

    return resources, errors


# ═════════════════════════════════════════════════════════════════════
# 근거 태깅 카운트 (근거 원장용)
# ═════════════════════════════════════════════════════════════════════

import re as _re
_GROUNDED_RE = _re.compile(r"\[근거:\s*([^\]]+)\]")
_SPECULATED_RE = _re.compile(r"\[추측\]")


def count_grounding(text: str) -> Dict:
    """에이전트 출력에서 [근거: 파일] / [추측] 태그 수를 계산."""
    grounded = _GROUNDED_RE.findall(text or "")
    speculated = len(_SPECULATED_RE.findall(text or ""))
    by_file: Dict[str, int] = {}
    for tag in grounded:
        fname = tag.strip()
        by_file[fname] = by_file.get(fname, 0) + 1
    return {
        "grounded_total": len(grounded),
        "speculated_total": speculated,
        "by_file": by_file,
    }
