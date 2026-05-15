"""세션 영속성 모듈 — 프로젝트 단위 JSON 저장/복원.

설계 원칙:
- 데이터베이스 없음. .sessions/ 디렉토리 + JSON 파일.
- 파일당 한 프로젝트. 한 프로젝트는 여러 버전(v1, v2...)을 가짐.
- 개인 노트북 전용 — 멀티유저/인증 없음.
"""

from __future__ import annotations

import json
import os
import re
import datetime
from pathlib import Path
from typing import Dict, List, Optional


SESSIONS_DIR = Path(__file__).parent / ".sessions"


def _slugify(text: str) -> str:
    """파일명으로 사용 가능한 slug 생성 (한글 허용)."""
    text = (text or "untitled").strip()
    text = re.sub(r"[/\\\?%*:|\"<>\n\t]", "", text)
    text = re.sub(r"\s+", "_", text)
    return text[:40] or "untitled"


def ensure_dir() -> None:
    SESSIONS_DIR.mkdir(parents=True, exist_ok=True)


# ═════════════════════════════════════════════════════════════════════
# 저장 / 로드
# ═════════════════════════════════════════════════════════════════════

def save_session(project_name: str, state: Dict, existing_path: Optional[str] = None) -> str:
    """세션 저장. 기존 경로가 있으면 덮어씀(버전 append), 없으면 새 파일 생성.

    state 구조:
      {
        "project_name": str,
        "created_at": ISO,
        "updated_at": ISO,
        "inputs": {field, stage, keywords, context, extra, advisor_mode},
        "resources_manifest": [{filename, chars, kind}],
        "versions": [
          {"version": 1, "ts": ISO, "stage": "...", "model": "...",
           "outputs": {"scout": "...", "critic": "...", "director": "...", "advisor": "..."}},
          ...
        ],
        "last_exports": {"docx": path, ...}
      }
    Returns the JSON file path.
    """
    ensure_dir()
    now = datetime.datetime.now().isoformat(timespec="seconds")
    state.setdefault("project_name", project_name)
    state.setdefault("created_at", now)
    state["updated_at"] = now

    if existing_path and Path(existing_path).exists():
        path = Path(existing_path)
    else:
        slug = _slugify(project_name)
        stamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
        path = SESSIONS_DIR / f"{stamp}_{slug}.json"

    path.write_text(json.dumps(state, ensure_ascii=False, indent=2), encoding="utf-8")
    return str(path)


def load_session(path: str) -> Dict:
    raw = Path(path).read_text(encoding="utf-8")
    return json.loads(raw)


def list_sessions() -> List[Dict]:
    """최근 세션 목록 반환. 메타데이터만."""
    ensure_dir()
    out: List[Dict] = []
    for p in sorted(SESSIONS_DIR.glob("*.json"), key=lambda x: x.stat().st_mtime, reverse=True):
        try:
            data = json.loads(p.read_text(encoding="utf-8"))
            out.append({
                "path": str(p),
                "filename": p.name,
                "project_name": data.get("project_name", p.stem),
                "updated_at": data.get("updated_at", ""),
                "version_count": len(data.get("versions", [])),
                "stage": data.get("inputs", {}).get("stage", "") or (
                    data.get("versions", [{}])[-1].get("stage", "") if data.get("versions") else ""
                ),
            })
        except Exception:
            continue
    return out


# ═════════════════════════════════════════════════════════════════════
# 버전 조작
# ═════════════════════════════════════════════════════════════════════

def new_version_entry(stage: str, model: str, outputs: Dict[str, str], note: str = "") -> Dict:
    return {
        "version": 0,  # caller will assign
        "ts": datetime.datetime.now().isoformat(timespec="seconds"),
        "stage": stage,
        "model": model,
        "outputs": outputs,
        "note": note,
    }


def append_version(state: Dict, entry: Dict) -> Dict:
    state.setdefault("versions", [])
    entry["version"] = len(state["versions"]) + 1
    state["versions"].append(entry)
    return entry


def latest_outputs(state: Dict) -> Dict[str, str]:
    versions = state.get("versions", [])
    if not versions:
        return {}
    return versions[-1].get("outputs", {})


def two_latest(state: Dict) -> List[Dict]:
    """Return latest 2 versions (oldest first). For v1/v2 tab comparison."""
    versions = state.get("versions", [])
    return versions[-2:]
