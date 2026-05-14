#!/usr/bin/env python3
"""Speculative Design Council — AI Speculative Design Council (Harness Engineering Demo).

변경 (v2):
- 단계별 프롬프트 트리오 (주제 탐색 / 선행연구 정리 / RQ 도출) 자동 라우팅
- 로컬 자료 업로드 (PDF·md·txt) → 에이전트가 근거 태깅 [근거:파일]/[추측]
- 세션 영속성 (.sessions/*.json) + v1↔v2 비교
- 대화형 정제 (특정 에이전트만 재실행, 버전 증가)
- 미래학자 페르소나 (선택 체크박스) + 회의 1-pager 산출
- 다중 산출물 메뉴 (docx / 회의 1p / 검색 쿼리 / IRB 카드 / BibTeX seed)

핵심 메시지: 같은 하네스, 다른 프롬프트. 코드 변경 없이 프롬프트만으로
3개 연구 단계를 각각 최적화된 3-에이전트 파이프라인으로 처리한다.
"""

from __future__ import annotations

import datetime
import re

import ollama
import streamlit as st

from agents import STAGE_PROMPTS, ADVISOR_PROMPT, ROLE_LABELS, get_prompt
import personas as personas_mod
from templates import (
    RESEARCH_FIELDS, RESEARCH_STAGES, REQUIRED_ITEMS,
    CONTEXT_PLACEHOLDER, KEYWORDS_PLACEHOLDER, EXTRA_PLACEHOLDER,
    RESOURCES_HELP, PROJECT_NAME_PLACEHOLDER,
    DOCX_HEADER, DOCX_DISCLAIMER, EXPORT_LABELS,
    DEMO_PROJECT_NAME, DEMO_INPUTS, DEMO_RESOURCE_PATH, DEMO_RESOURCE_FILENAME,
)
from resources import (
    ingest_uploads, build_resource_block, resources_manifest,
    count_grounding, MAX_FILES,
)
from sessions import (
    save_session, load_session, list_sessions,
    new_version_entry, append_version, latest_outputs, two_latest,
)
from exporters import EXPORT_REGISTRY, create_docx


# ═════════════════════════════════════════════════════════════════════
# CSS (동일; 일부 추가)
# ═════════════════════════════════════════════════════════════════════

CUSTOM_CSS = """
<style>
@import url('https://fonts.googleapis.com/css2?family=Noto+Serif+KR:wght@400;600;700&family=Noto+Sans+KR:wght@300;400;500;600&family=IBM+Plex+Mono:wght@400;500&display=swap');

:root {
    --ink: #1a1a1a;
    --ink-light: #4a4a4a;
    --ink-muted: #8a8a8a;
    --paper: #faf8f5;
    --paper-warm: #f5f0e8;
    --paper-cool: #f0efe9;
    --accent: #2c5f7c;
    --accent-deep: #1a3d52;
    --accent-light: #e8f0f5;
    --verify-green: #2d6a4f;
    --verify-green-bg: #edf5f0;
    --warn-amber: #8b6914;
    --warn-amber-bg: #fdf6e3;
    --fail-red: #9b2c2c;
    --fail-red-bg: #fef2f2;
    --rule: #d4cfc4;
    --rule-light: #e8e4db;
}

.stApp { background-color: var(--paper) !important; }

section[data-testid="stSidebar"] {
    background-color: var(--paper-cool) !important;
    border-right: 1px solid var(--rule) !important;
}

section[data-testid="stSidebar"] .stMarkdown p,
section[data-testid="stSidebar"] .stMarkdown li {
    font-family: 'Noto Sans KR', sans-serif !important;
    font-size: 0.85rem !important;
    color: var(--ink-light) !important;
}

h1, h2, h3 {
    font-family: 'Noto Serif KR', 'Georgia', serif !important;
    color: var(--ink) !important;
    letter-spacing: -0.01em !important;
}
h1 { font-weight: 700 !important; font-size: 1.8rem !important; border-bottom: 2px solid var(--ink) !important; padding-bottom: 0.4rem !important; margin-bottom: 0.3rem !important; }
h2 { font-weight: 600 !important; font-size: 1.25rem !important; color: var(--accent-deep) !important; }
h3 { font-weight: 600 !important; font-size: 1.05rem !important; }

p, li, label, .stMarkdown {
    font-family: 'Noto Sans KR', sans-serif !important;
    color: var(--ink-light) !important;
    line-height: 1.7 !important;
}
code, .stCode, pre { font-family: 'IBM Plex Mono', monospace !important; }

hr { border: none !important; border-top: 1px solid var(--rule) !important; margin: 1.5rem 0 !important; }

.stButton > button[kind="primary"] {
    background-color: var(--accent-deep) !important;
    color: #ffffff !important;
    border: none !important;
    border-radius: 4px !important;
    font-family: 'Noto Sans KR', sans-serif !important;
    font-weight: 600 !important;
    font-size: 1.0rem !important;
    letter-spacing: 0.04em !important;
    padding: 0.75rem 1.5rem !important;
}
.stButton > button[kind="primary"] *,
.stButton > button[kind="primary"] p,
.stButton > button[kind="primary"] div {
    color: #ffffff !important;
    font-weight: 600 !important;
}
.stButton > button[kind="primary"]:hover {
    background-color: var(--accent) !important;
}
.stButton > button[kind="primary"]:hover *,
.stButton > button[kind="primary"]:hover p {
    color: #ffffff !important;
}

.stButton > button:not([kind="primary"]) {
    background-color: #ffffff !important;
    color: var(--accent-deep) !important;
    border: 1px solid var(--accent-deep) !important;
    border-radius: 4px !important;
    font-family: 'Noto Sans KR', sans-serif !important;
    font-size: 0.88rem !important;
    font-weight: 500 !important;
}
.stButton > button:not([kind="primary"]) *,
.stButton > button:not([kind="primary"]) p,
.stButton > button:not([kind="primary"]) div {
    color: var(--accent-deep) !important;
}
.stButton > button:not([kind="primary"]):hover {
    background-color: var(--accent-light) !important;
    border-color: var(--accent) !important;
}

.stTextInput > div > div > input,
.stTextArea > div > div > textarea,
.stSelectbox > div > div {
    background-color: #fff !important;
    border: 1px solid var(--rule) !important;
    border-radius: 2px !important;
    font-family: 'Noto Sans KR', sans-serif !important;
    color: var(--ink) !important;
    font-size: 0.9rem !important;
}

.streamlit-expanderHeader {
    font-family: 'Noto Sans KR', sans-serif !important;
    font-weight: 500 !important;
    font-size: 0.9rem !important;
    color: var(--ink) !important;
    background-color: var(--paper-warm) !important;
    border: 1px solid var(--rule-light) !important;
    border-radius: 2px !important;
}

.stAlert > div {
    border-radius: 2px !important;
    font-family: 'Noto Sans KR', sans-serif !important;
    font-size: 0.85rem !important;
}

.stDownloadButton > button {
    background-color: var(--verify-green) !important;
    color: #fff !important;
    border: none !important;
    border-radius: 2px !important;
    font-family: 'Noto Sans KR', sans-serif !important;
    font-weight: 500 !important;
}

.masthead { padding: 0.2rem 0 0.8rem 0; margin-bottom: 1.2rem; }
.masthead-sub { font-family: 'IBM Plex Mono', monospace; font-size: 0.72rem; color: var(--ink-muted); letter-spacing: 0.12em; text-transform: uppercase; margin-bottom: 0.3rem; }
.masthead-title { font-family: 'Noto Serif KR', serif; font-size: 1.9rem; font-weight: 700; color: var(--ink); line-height: 1.2; letter-spacing: -0.02em; margin: 0; }
.masthead-desc { font-family: 'Noto Sans KR', sans-serif; font-size: 0.88rem; color: var(--ink-light); margin-top: 0.5rem; line-height: 1.6; }
.masthead-rule { border: none; border-top: 2px solid var(--ink); margin: 0.8rem 0 0 0; width: 100%; }

.pipeline-step {
    background: var(--paper-warm);
    border: 1px solid var(--rule);
    border-radius: 2px;
    padding: 1rem 1.2rem;
    height: 100%;
}
.pipeline-step-num { font-family: 'IBM Plex Mono', monospace; font-size: 0.65rem; color: var(--ink-muted); letter-spacing: 0.1em; text-transform: uppercase; margin-bottom: 0.25rem; }
.pipeline-step-name { font-family: 'Noto Serif KR', serif; font-size: 1.05rem; font-weight: 600; color: var(--ink); margin-bottom: 0.2rem; }
.pipeline-step-role { font-family: 'Noto Sans KR', sans-serif; font-size: 0.75rem; color: var(--ink-muted); line-height: 1.4; }
.pipeline-step-status { font-family: 'IBM Plex Mono', monospace; font-size: 0.7rem; margin-top: 0.5rem; padding: 0.15rem 0.5rem; border-radius: 1px; display: inline-block; }
.status-waiting { color: var(--ink-muted); background: var(--paper); border: 1px solid var(--rule-light); }
.status-active { color: var(--accent-deep); background: var(--accent-light); border: 1px solid var(--accent); animation: pulse-subtle 2s infinite; }
.status-done { color: var(--verify-green); background: var(--verify-green-bg); border: 1px solid #b7d7c2; }
@keyframes pulse-subtle { 0%,100% { opacity: 1;} 50% { opacity: 0.7; } }

.disclaimer-box {
    background: var(--paper-warm);
    border-left: 3px solid var(--warn-amber);
    padding: 0.6rem 1rem;
    margin: 0.8rem 0 1.2rem 0;
    font-family: 'Noto Sans KR', sans-serif;
    font-size: 0.8rem;
    color: var(--ink-light);
    border-radius: 0 2px 2px 0;
}

.result-header {
    font-family: 'Noto Serif KR', serif;
    font-size: 1.1rem;
    font-weight: 600;
    color: var(--ink);
    border-bottom: 1px solid var(--rule);
    padding-bottom: 0.3rem;
    margin: 1.5rem 0 0.8rem 0;
}

.section-label { font-family: 'IBM Plex Mono', monospace; font-size: 0.65rem; color: var(--ink-muted); letter-spacing: 0.15em; text-transform: uppercase; margin-bottom: 0.5rem; }

.completion-banner {
    background: var(--verify-green-bg);
    border: 1px solid #b7d7c2;
    border-left: 4px solid var(--verify-green);
    padding: 1rem 1.2rem;
    border-radius: 0 2px 2px 0;
    margin: 1rem 0;
}
.completion-banner-title { font-family: 'Noto Serif KR', serif; font-size: 1rem; font-weight: 600; color: var(--verify-green); margin-bottom: 0.3rem; }
.completion-banner-desc { font-family: 'Noto Sans KR', sans-serif; font-size: 0.82rem; color: var(--ink-light); }

.harness-note {
    background: var(--paper-cool);
    border: 1px solid var(--rule);
    padding: 0.8rem 1rem;
    margin: 1rem 0;
    border-radius: 2px;
}
.harness-note-title { font-family: 'IBM Plex Mono', monospace; font-size: 0.7rem; color: var(--accent); letter-spacing: 0.08em; text-transform: uppercase; margin-bottom: 0.3rem; }
.harness-note-text { font-family: 'Noto Sans KR', sans-serif; font-size: 0.82rem; color: var(--ink-light); line-height: 1.6; }

.sidebar-brand { font-family: 'Noto Serif KR', serif; font-size: 1rem; font-weight: 600; color: var(--ink); margin-bottom: 0.1rem; }
.sidebar-brand-sub { font-family: 'IBM Plex Mono', monospace; font-size: 0.6rem; color: var(--ink-muted); letter-spacing: 0.1em; text-transform: uppercase; }

.sidebar-status {
    display: flex; align-items: center; gap: 0.4rem;
    padding: 0.4rem 0.6rem;
    border-radius: 2px;
    font-family: 'IBM Plex Mono', monospace;
    font-size: 0.75rem;
    margin: 0.5rem 0;
}
.sidebar-status-ok { background: var(--verify-green-bg); color: var(--verify-green); border: 1px solid #b7d7c2; }
.sidebar-status-err { background: var(--fail-red-bg); color: var(--fail-red); border: 1px solid #f5c6c6; }

.footer-note {
    font-family: 'IBM Plex Mono', monospace;
    font-size: 0.6rem;
    color: var(--ink-muted);
    text-align: center;
    margin-top: 2rem;
    padding-top: 0.8rem;
    border-top: 1px solid var(--rule-light);
    letter-spacing: 0.05em;
}

/* v2 추가 */
.ledger-card {
    background: var(--paper-warm);
    border: 1px solid var(--rule);
    border-radius: 2px;
    padding: 0.6rem 0.9rem;
    margin: 0.5rem 0;
    font-family: 'IBM Plex Mono', monospace;
    font-size: 0.78rem;
    color: var(--ink-light);
}
.ledger-grounded { color: var(--verify-green); font-weight: 500; }
.ledger-speculated { color: var(--warn-amber); font-weight: 500; }

.resource-chip {
    display: inline-block;
    background: var(--accent-light);
    color: var(--accent-deep);
    border: 1px solid var(--accent);
    border-radius: 999px;
    padding: 0.1rem 0.7rem;
    margin: 0.1rem 0.2rem 0.1rem 0;
    font-family: 'IBM Plex Mono', monospace;
    font-size: 0.7rem;
}
</style>
"""


# ═════════════════════════════════════════════════════════════════════
# Ollama 연결 & 모델 목록 — 한 번의 호출로 병합
# ═════════════════════════════════════════════════════════════════════

def fetch_ollama_state():
    """Return (connected, models_list). models_list is [(name, size_gb), ...].
    Dedupes tags pointing to the same digest (e.g. gemma4:26b is an alias for
    gemma4:26b-a4b-it-q4_K_M — we show the shorter tag only)."""
    try:
        result = ollama.list()
    except Exception:
        return False, []

    models_raw = []
    if hasattr(result, "models"):
        models_raw = [
            (m.model, getattr(m, "size", 0), getattr(m, "digest", "") or "")
            for m in result.models
        ]
    elif isinstance(result, dict) and "models" in result:
        models_raw = [
            (m["name"], m.get("size", 0), m.get("digest", ""))
            for m in result["models"]
        ]

    # Dedupe by digest — keep the shortest tag name per digest (most canonical)
    by_digest: dict = {}
    no_digest: list = []
    for name, size, digest in models_raw:
        if "embed" in name.lower() or "nomic" in name.lower():
            continue
        if not digest:
            no_digest.append((name, size))
            continue
        current = by_digest.get(digest)
        if current is None or len(name) < len(current[0]):
            by_digest[digest] = (name, size)

    models = [(name, (size / (1024 ** 3)) if size else 0)
              for name, size in list(by_digest.values()) + no_digest]
    models.sort(key=lambda x: x[1], reverse=True)
    return True, models


def format_model_size(gb: float) -> str:
    if gb < 1:
        return f"{gb * 1024:.0f}MB"
    return f"{gb:.1f}GB"


# ═════════════════════════════════════════════════════════════════════
# Ollama 호출 — 스트리밍
# ═════════════════════════════════════════════════════════════════════

THINKING_TIMEOUT_HINT = (
    "⚠️ 모델이 최종 응답을 생성하기 전에 예산이 소진되었습니다. "
    "사고 모드를 끄거나(빠른 모드) num_predict 를 더 크게 설정하세요."
)


def strip_code_fences(text: str) -> str:
    """Remove stray ```markdown / ``` code fences from LLM output.

    Many LLMs wrap markdown output in triple-backtick fences despite instructions.
    This strips them so the rendered markdown looks clean and the export files
    don't carry junk fence markers.
    """
    if not text:
        return text
    import re
    # Strip "```markdown" or "```md" or "```" at start of line, including trailing newline
    text = re.sub(r'^\s*```(?:markdown|md)?\s*\n?', '', text, flags=re.MULTILINE)
    # Strip "```" at end of line
    text = re.sub(r'\n?\s*```\s*$', '', text, flags=re.MULTILINE)
    return text


def run_streamed(stream_iter, content_placeholder, thinking_placeholder=None):
    """Consume a stream_ollama iterator, routing chunks to placeholders.
    Returns the accumulated content text (thinking is shown separately but not stored
    in the final artifact — only final 'content' is persisted).
    Code fences are stripped from final output."""
    content = ""
    thinking = ""
    for chunk in stream_iter:
        if chunk["kind"] == "thinking" and thinking_placeholder is not None:
            thinking += chunk["text"]
            # Truncate thinking display to last ~800 chars to keep it bounded
            tail = thinking[-800:]
            thinking_placeholder.markdown(
                f"<div style='background:#f0efe9;border-left:3px solid #8a8a8a;"
                f"padding:0.5rem 0.8rem;margin:0.3rem 0;font-family:IBM Plex Mono,monospace;"
                f"font-size:0.72rem;color:#4a4a4a;white-space:pre-wrap;max-height:180px;"
                f"overflow-y:auto;'>사고 중…<br>{tail}</div>",
                unsafe_allow_html=True,
            )
        elif chunk["kind"] == "content":
            content += chunk["text"]
            content_placeholder.markdown(strip_code_fences(content) + " ●")
    final = strip_code_fences(content)
    content_placeholder.markdown(final)
    return final


def stream_ollama(model: str, system_prompt: str, user_prompt: str,
                  think: bool = False, num_predict: int = 4096,
                  keep_alive: int = 0):
    """Stream chat chunks. Yields dicts: {'kind': 'content'|'thinking', 'text': str}.
    When think=False, only 'content' is yielded. When think=True, 'thinking' chunks
    stream first (reasoning), then 'content' chunks (final answer).
    keep_alive=0 unloads the model after the call — lets downstream agents load fresh
    without VRAM thrashing (sequential orchestration hygiene)."""
    # Thinking needs a lot more headroom — verified empirically: 3500 tokens wasn't
    # enough for a 1-sentence prompt, 10K thinking chars were generated then cut off.
    # Bump to 12K when thinking is on so final content has room to emerge.
    effective_budget = max(num_predict, 12288) if think else num_predict
    response = ollama.chat(
        model=model,
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt},
        ],
        think=think,
        options={"temperature": 0.3, "top_p": 0.9, "num_predict": effective_budget},
        keep_alive=keep_alive,
        stream=True,
    )
    total_content = 0
    for chunk in response:
        msg = chunk.message if hasattr(chunk, "message") else chunk.get("message")
        if msg is None:
            continue
        content = (msg.content if hasattr(msg, "content") else msg.get("content")) or ""
        thinking = (msg.thinking if hasattr(msg, "thinking") else msg.get("thinking")) or ""
        if thinking:
            yield {"kind": "thinking", "text": thinking}
        if content:
            total_content += len(content)
            yield {"kind": "content", "text": content}
    if total_content == 0:
        yield {"kind": "content", "text": "\n\n" + THINKING_TIMEOUT_HINT}


# ═════════════════════════════════════════════════════════════════════
# 파이프라인 시각화
# ═════════════════════════════════════════════════════════════════════

PIPELINE_ROLES = [
    ("Step I",   "거울", "확장",   "scout",    "narratype 4-archetype 확장"),
    ("Step II",  "지도", "비평",   "critic",   "구조·권력·사각지대 분석"),
    ("Step III", "의장", "종합",   "director", "Council deliberation 종합 판단"),
]


def render_pipeline(step: int, advisor_mode: bool) -> None:
    """Render 3 (or 4) pipeline steps. step: 1=scout running .. 5=done."""
    cols = st.columns(4 if advisor_mode else 3)

    items = list(PIPELINE_ROLES)
    if advisor_mode:
        items.append(("Step IV", "하나", "미래학자", "advisor", "Dator 4 archetypes 메타 질문 10개"))

    for i, (label, name, role_label, role_key, desc) in enumerate(items):
        s = i + 1
        if step > s:
            status_class, status_text = "status-done", "COMPLETE"
        elif step == s:
            status_class, status_text = "status-active", "PROCESSING..."
        else:
            status_class, status_text = "status-waiting", "STANDBY"
        with cols[i]:
            st.markdown(
                f'<div class="pipeline-step">'
                f'<div class="pipeline-step-num">{label}</div>'
                f'<div class="pipeline-step-name">{name} ({role_label})</div>'
                f'<div class="pipeline-step-role">{desc}</div>'
                f'<div class="pipeline-step-status {status_class}">{status_text}</div>'
                f'</div>',
                unsafe_allow_html=True,
            )


# ═════════════════════════════════════════════════════════════════════
# 근거 원장 (grounding ledger) 렌더
# ═════════════════════════════════════════════════════════════════════

def render_ledger(text: str) -> None:
    stats = count_grounding(text)
    if stats["grounded_total"] == 0 and stats["speculated_total"] == 0:
        return
    parts = []
    parts.append(f'<span class="ledger-grounded">근거 {stats["grounded_total"]}건</span>')
    parts.append(f'<span class="ledger-speculated">추측 {stats["speculated_total"]}건</span>')
    if stats["by_file"]:
        files_part = " · ".join(
            f"{f}×{n}" for f, n in sorted(stats["by_file"].items(), key=lambda x: -x[1])[:5]
        )
        parts.append(f'<span style="color:var(--ink-muted)">{files_part}</span>')
    st.markdown(
        f'<div class="ledger-card">근거 원장: {" · ".join(parts)}</div>',
        unsafe_allow_html=True,
    )


# ═════════════════════════════════════════════════════════════════════
# 사용자 프롬프트 조립
# ═════════════════════════════════════════════════════════════════════

def build_user_payload(inputs: dict, resources: list, resource_override: list = None) -> str:
    rs = resource_override if resource_override is not None else resources
    resource_block = build_resource_block(rs)
    # N-round: inject previous director output if this is round 2+
    prior_block = ""
    try:
        rh = st.session_state.get("round_history", [])
        cur = st.session_state.get("current_round", 1)
        if rh and cur > 1:
            last = rh[-1]
            prior_block = (
                f"=== 이전 라운드 ({last['round']}) 의장 종합 결과 ===\n"
                f"{last.get('director', '')}\n"
                f"=== 이전 라운드 끝 ===\n\n"
                "★ 이번 라운드는 위 이전 의장 결과를 받아 **더 깊이·다른 각도**로 확장하세요. "
                "단순 반복 금지. 새 archetype·인물·기술·균열을 추가하거나, 이전 결과의 약점을 명시적으로 보강.\n\n"
            )
    except Exception:
        pass
    return (
        prior_block
        + resource_block
        + "=== 연구 맥락 ===\n"
        + f"연구 분야: {inputs['field']}\n"
        + f"연구 단계: {inputs['stage']}\n"
        + f"키워드: {inputs['keywords']}\n"
        + f"상세 맥락: {inputs['context']}\n"
        + "=== 맥락 끝 ===\n\n"
        + f"=== 추가 요청 ===\n{inputs.get('extra') or '없음'}\n=== 요청 끝 ===\n\n"
        + "★ 위 맥락의 모든 정보를 결과물에 직접 반영하세요. "
        "업로드 자료에서 근거를 찾을 수 있으면 [근거: 파일명] 태그를, "
        "없으면 [추측] 태그를 붙이세요."
    )


def build_critic_payload(inputs, resources, scout_output) -> str:
    base = build_user_payload(inputs, resources)
    return (
        f"=== 거울의 탐색 결과 ===\n{scout_output}\n=== 결과 끝 ===\n\n"
        + base
        + "\n\n★ 최우선: 거울의 결과에서 추상·SF tropes 회귀·기술 결정론·사각지대를 적극 비평하세요. "
        "기존 주장에 동의하지 마세요."
    )


def build_director_payload(inputs, resources, scout_output, critic_output) -> str:
    base = build_user_payload(inputs, resources)
    return (
        f"=== 거울의 탐색 결과 ===\n{scout_output}\n=== 탐색 끝 ===\n\n"
        f"=== 지도의 검증 결과 ===\n{critic_output}\n=== 검증 끝 ===\n\n"
        + base
        + "\n\n★ 최종 종합: 지도의 /⚠️ 항목을 모두 반영하고, "
        "업로드 자료가 있으면 근거 무결성을 재확인하세요."
    )


def build_advisor_payload(inputs, director_output) -> str:
    return (
        f"=== 학생이 준비한 Council 분석 ===\n{director_output}\n=== 설계 끝 ===\n\n"
        f"=== 학생 배경 ===\n분야: {inputs['field']} / 단계: {inputs['stage']}\n"
        f"키워드: {inputs['keywords']}\n=== 배경 끝 ===\n\n"
        "★ 미래학자(하나)로서 Dator 4 archetypes (성장/붕괴/지속/변혁) lens로 메타 질문 10개를 생성하세요."
    )


# ═════════════════════════════════════════════════════════════════════
# 세션 상태 초기화/리셋
# ═════════════════════════════════════════════════════════════════════

DEFAULT_STATE = {
    "step": 0,                      # 0=idle, 1..4=running scout/critic/director/advisor, 5=done
    "scout_output": "",
    "critic_output": "",
    "director_output": "",
    "advisor_output": "",
    "resources": [],                # [{filename, text}]
    "inputs_snapshot": {},          # frozen at pipeline start
    "advisor_mode": False,
    "think_mode": False,            # thinking mode — slower but deeper reasoning
    "session_path": None,           # existing session JSON path, if resumed
    "project_name": "",
    "session_state_dict": None,     # the full saved-state dict
    "refine_target": "",            # role key for refinement ('scout'/'critic'/'director'/'advisor')
    "refine_feedback": "",
    "refine_running": False,
    "refine_version_marker": False, # True when latest version was a refinement (for v1↔v2 tabs)
    "model": "",
    # A/B 대조 실행 — 동일 파이프라인을 자료 없이 한 번 더 돌려 차이를 시각화
    "ab_step": 0,                   # 0=idle, 1=scout, 2=critic, 3=director, 4=done
    "ab_scout_output": "",
    "ab_critic_output": "",
    "ab_director_output": "",
    # 에이전트별 모델 지정 — 하네스 엔지니어링의 또 다른 축
    # (같은 프롬프트, 다른 모델) : scout=빠른·표면, critic=사고·반증, director=한국어·종합
    "per_agent_mode": False,
    "agent_models": {},             # {'scout': 'gemma4', 'critic': 'deepseek-r1:14b', ...}
    # Nemotron persona Council (Option D)
    "personas_pool": [],            # list of persona dicts loaded from xlsx/json
    "personas_filename": "",        # display name of uploaded persona file
    "council": {},                  # {'scout': persona_dict, 'critic': ..., 'director': ..., 'advisor': ...}
    "council_mode": False,          # True if persona-driven Council active
    # N-Round iteration (Option D from N-round design)
    "n_rounds": 1,                  # total rounds (1-5). 1 = current single-pass behavior
    "current_round": 1,             # which round is currently running (1..n_rounds)
    "round_history": [],            # list of {round: int, scout, critic, director} for completed rounds
    # Language (i18n)
    "language": "ko",               # 'ko' or 'en' — controls UI + LLM output language
}


ROLE_ORDER = ["scout", "critic", "director", "advisor"]


def get_personified_prompt(stage: str, role: str) -> str:
    """Wrap base stage/role prompt with persona identity if Council is composed.

    Backward compatible: no Council -> returns base prompt unchanged.
    Language directive auto-injected by get_prompt() based on session_state.language.
    """
    lang = st.session_state.get("language", "ko")
    base = get_prompt(stage, role, language=lang)
    if not st.session_state.get("council_mode"):
        return base
    council = st.session_state.get("council") or {}
    persona = council.get(role)
    return personas_mod.make_personified_prompt(role, base, persona)


def get_personified_advisor_prompt() -> str:
    """Wrap ADVISOR_PROMPT with persona if Council composed. Language directive appended."""
    from agents import language_directive
    lang = st.session_state.get("language", "ko")
    base = ADVISOR_PROMPT + language_directive(lang)
    if not st.session_state.get("council_mode"):
        return base
    council = st.session_state.get("council") or {}
    persona = council.get("advisor")
    return personas_mod.make_personified_prompt("advisor", base, persona)


def pick_model(role: str, fallback: str) -> str:
    """Return the model to use for a given role.

    - If per_agent_mode is on: use agent_models map (full per-role control).
    - If per_agent_mode is off BUT role == 'advisor' AND advisor has its own model set:
      use it (this lets the advisor-mode picker work without forcing per_agent_mode).
    - Else: fallback (sidebar's primary model).
    """
    if st.session_state.get("per_agent_mode"):
        return st.session_state.agent_models.get(role, fallback)
    # Special case: advisor has a dedicated picker shown next to its toggle
    if role == "advisor":
        adv = st.session_state.agent_models.get("advisor")
        if adv:
            return adv
    return fallback


def init_state():
    for k, v in DEFAULT_STATE.items():
        if k not in st.session_state:
            st.session_state[k] = v if not isinstance(v, (list, dict)) else (list(v) if isinstance(v, list) else dict(v))


def reset_pipeline_outputs():
    st.session_state.step = 0
    st.session_state.scout_output = ""
    st.session_state.critic_output = ""
    st.session_state.director_output = ""
    st.session_state.advisor_output = ""


def reset_session():
    for k, v in DEFAULT_STATE.items():
        st.session_state[k] = v if not isinstance(v, (list, dict)) else (list(v) if isinstance(v, list) else dict(v))


def load_demo_scenario(scenario_key: str = "happy_gate"):
    """Populate state with a demo scenario (2025 학생 narratype).

    scenario_key: one of DEMO_SCENARIOS keys (happy_gate / cocoo / split / selecton).
    """
    from templates import DEMO_SCENARIOS
    reset_session()
    scenario = DEMO_SCENARIOS.get(scenario_key, DEMO_SCENARIOS["happy_gate"])
    st.session_state.project_name = scenario["project_name"]
    st.session_state.inputs_snapshot = {
        "field": scenario["field"],
        "stage": scenario["stage"],
        "context": scenario["context"],
        "keywords": scenario["keywords"],
        "extra": scenario["extra"],
    }
    st.session_state.resources = []  # 데모는 별도 자료 없이 작동


# ═════════════════════════════════════════════════════════════════════
# 세션 저장/복원
# ═════════════════════════════════════════════════════════════════════

def persist_current_version(note: str = "") -> None:
    """Snapshot current pipeline outputs as a new version entry in the state dict, save to disk."""
    state = st.session_state.session_state_dict or {
        "project_name": st.session_state.project_name or "untitled",
        "inputs": dict(st.session_state.inputs_snapshot),
        "resources_manifest": resources_manifest(st.session_state.resources),
        "versions": [],
    }
    state["inputs"] = dict(st.session_state.inputs_snapshot)
    state["resources_manifest"] = resources_manifest(st.session_state.resources)
    # Record per-agent model split if advanced mode was in use
    if st.session_state.per_agent_mode:
        state["agent_models"] = dict(st.session_state.agent_models)
    else:
        state.pop("agent_models", None)

    model_descriptor = st.session_state.model or ""
    if st.session_state.per_agent_mode and st.session_state.agent_models:
        model_descriptor = "mixed: " + " · ".join(
            f"{r}={m}" for r, m in st.session_state.agent_models.items()
        )
    entry = new_version_entry(
        stage=st.session_state.inputs_snapshot.get("stage", ""),
        model=model_descriptor,
        outputs={
            "scout": st.session_state.scout_output,
            "critic": st.session_state.critic_output,
            "director": st.session_state.director_output,
            "advisor": st.session_state.advisor_output,
        },
        note=note,
    )
    append_version(state, entry)

    path = save_session(state["project_name"], state, existing_path=st.session_state.session_path)
    st.session_state.session_path = path
    st.session_state.session_state_dict = state


def hydrate_from_session(path: str) -> None:
    data = load_session(path)
    reset_session()
    st.session_state.session_path = path
    st.session_state.session_state_dict = data
    st.session_state.project_name = data.get("project_name", "")
    st.session_state.inputs_snapshot = data.get("inputs", {})
    st.session_state.advisor_mode = bool(data.get("inputs", {}).get("advisor_mode", False))
    if "agent_models" in data:
        st.session_state.agent_models = dict(data["agent_models"])
        st.session_state.per_agent_mode = True
    latest = latest_outputs(data)
    st.session_state.scout_output = latest.get("scout", "")
    st.session_state.critic_output = latest.get("critic", "")
    st.session_state.director_output = latest.get("director", "")
    st.session_state.advisor_output = latest.get("advisor", "")
    st.session_state.step = 5 if st.session_state.director_output else 0


# ═════════════════════════════════════════════════════════════════════
# 최종 Council 분석 텍스트 추출 (의장 출력 중 '최종 Council 분석' 섹션)
# ═════════════════════════════════════════════════════════════════════

def extract_final_doc(director_output: str) -> str:
    """Return the body under the heading (최종 Council 분석 / 확정 RQ / 선행연구 종합 메모).
    Falls back to full output if the expected section bars aren't found."""
    if not director_output:
        return ""
    # Section pattern: heading → ━ separator → body → next ━ (or end)
    specific = r"[^\n]*\n━+\s*\n(.*?)(?=\n━+|\Z)"
    m = re.search(specific, director_output, re.DOTALL)
    if m and m.group(1).strip():
        return m.group(1).strip()
    # Fallback: any heading and everything after it
    loose = r"[^\n]*\n(.*?)(?=\n━+|\Z)"
    m = re.search(loose, director_output, re.DOTALL)
    if m and m.group(1).strip():
        return m.group(1).strip()
    return director_output.strip()


# ═════════════════════════════════════════════════════════════════════
# 메인 앱
# ═════════════════════════════════════════════════════════════════════

def main():
    st.set_page_config(
        page_title="Speculative Design Council",
        page_icon=None,
        layout="wide",
    )
    st.markdown(CUSTOM_CSS, unsafe_allow_html=True)
    init_state()

    # ── Ollama 연결 + 모델 목록 (단일 호출) ──
    is_connected, installed = fetch_ollama_state()

    # ─────────────────────────────────────────────
    # 사이드바
    # ─────────────────────────────────────────────
    with st.sidebar:
        st.markdown('<div class="sidebar-brand">SD Council</div>', unsafe_allow_html=True)
        st.markdown(
            '<div class="sidebar-brand-sub">Speculative Design Council · v2</div>',
            unsafe_allow_html=True,
        )

        # 언어 토글 — 최상단에 prominent
        lang_options = {"ko": "한국어", "en": "English"}
        cur_lang = st.session_state.get("language", "ko")
        lang_pick = st.radio(
            "언어 / Language",
            options=list(lang_options.keys()),
            format_func=lambda k: lang_options[k],
            index=0 if cur_lang == "ko" else 1,
            horizontal=True,
            key="language_radio",
            help="UI + LLM 출력 언어. ko=한국어, en=English. Demo scenarios are Korean-society narratypes but output language switches.",
        )
        st.session_state.language = lang_pick

        # i18n helper for this render
        from templates import tr as _tr
        def L(key):
            return _tr(key, st.session_state.language)

        st.markdown("---")

        # Ollama 상태
        if is_connected:
            st.markdown('<div class="sidebar-status sidebar-status-ok">Ollama 연결됨</div>', unsafe_allow_html=True)
        else:
            st.markdown('<div class="sidebar-status sidebar-status-err">Ollama 연결 실패</div>', unsafe_allow_html=True)
            st.code("ollama serve", language="bash")

        # 모델 선택 — 가장 작은 모델이 default (실수로 실행해도 부담 최소)
        st.markdown('<div class="section-label">모델 (작은 순)</div>', unsafe_allow_html=True)
        if installed:
            # Sort by size ascending — smallest first (default)
            installed_sorted = sorted(installed, key=lambda m: m[1] or 0)
            model_names = [m[0] for m in installed_sorted]
            model_captions = [format_model_size(m[1]) for m in installed_sorted]
            selected_model = st.radio(
                "모델 선택",
                model_names,
                index=0,
                captions=model_captions,
                label_visibility="collapsed",
                key="model_radio",
            )
            st.markdown(
                f'<div style="font-family:IBM Plex Mono,monospace;font-size:0.65rem;'
                f'color:#8a8a8a;margin-top:0.3rem;">{len(installed)} model(s) detected</div>',
                unsafe_allow_html=True,
            )
        else:
            selected_model = "gemma4"
            st.markdown(
                '<div style="font-family:Noto Sans KR,sans-serif;font-size:0.8rem;'
                'color:#8a8a8a;">모델이 없습니다.</div>',
                unsafe_allow_html=True,
            )
            st.code("ollama pull gemma4", language="bash")

        st.session_state.model = selected_model

        # 에이전트별 모델 지정 (고급 옵션)
        per_agent_on = st.checkbox(
            "️ 에이전트별 모델 지정 (고급)",
            value=st.session_state.per_agent_mode,
            help="역할마다 다른 모델을 할당합니다. 예: scout=gemma4(빠른 탐색), "
                 "critic=deepseek-r1(사고 기반 반증), director=qwen3.5(한국어 종합). "
                 "같은 하네스·다른 모델 — Harness Engineering 의 또 다른 축.",
        )
        st.session_state.per_agent_mode = per_agent_on

        if per_agent_on and installed:
            model_opts = [m[0] for m in installed]
            current = st.session_state.agent_models or {}
            st.markdown(
                '<div style="font-family:IBM Plex Mono,monospace;font-size:0.62rem;'
                'color:#8a8a8a;margin-top:0.4rem;">역할별 모델</div>',
                unsafe_allow_html=True,
            )
            for role in ROLE_ORDER:
                if role == "advisor" and not st.session_state.advisor_mode:
                    continue
                label_ko = ROLE_LABELS[role].split(" ")[0]
                default = current.get(role, selected_model)
                idx = model_opts.index(default) if default in model_opts else 0
                picked = st.selectbox(
                    f"{label_ko}",
                    model_opts,
                    index=idx,
                    key=f"agent_model_{role}",
                )
                st.session_state.agent_models[role] = picked

        st.markdown("---")

        # 세션 선택
        st.markdown('<div class="section-label">세션</div>', unsafe_allow_html=True)
        sessions = list_sessions()
        session_choices = ["새 프로젝트"] + [
            f"▸ {s['project_name']} (v{s['version_count']}) — {s['updated_at'][:16]}"
            for s in sessions
        ]
        session_idx = st.selectbox(
            "세션 선택",
            list(range(len(session_choices))),
            format_func=lambda i: session_choices[i],
            label_visibility="collapsed",
            key="session_select",
        )
        if session_idx > 0:
            candidate_path = sessions[session_idx - 1]["path"]
            if candidate_path != st.session_state.session_path:
                if st.button("이 세션 재개", key="resume_btn", use_container_width=True):
                    hydrate_from_session(candidate_path)
                    st.rerun()
        if st.button("새 세션 시작", key="new_btn", use_container_width=True):
            reset_session()
            st.rerun()

        st.markdown("---")

        # Council 구성 (Nemotron-Personas-Korea) — Option D
        st.markdown('<div class="section-label">Council 구성 (선택)</div>', unsafe_allow_html=True)
        st.caption("Nemotron-Personas-Korea Excel/JSON을 올리면, 추상 Council 대신 실제 demographic 페르소나가 거울/지도/의장/미래학자 역할을 연기합니다.")

        persona_file = st.file_uploader(
            "페르소나 파일 (.xlsx 또는 .json)",
            type=["xlsx", "json"],
            key="persona_uploader",
            help="첨부 'Nemotron-Personas-Korea 샘플 30명.xlsx' 또는 직접 만든 페르소나 풀.",
        )
        if persona_file is not None:
            try:
                pool = personas_mod.load_personas(persona_file)
                if pool and pool != st.session_state.personas_pool:
                    st.session_state.personas_pool = pool
                    st.session_state.personas_filename = persona_file.name
                    st.session_state.council = {}  # reset on new pool
                    st.session_state.council_mode = False
                    st.success(f"{len(pool)}명 페르소나 로드: {persona_file.name}")
            except Exception as e:
                st.error(f"페르소나 로드 실패: {e}")

        if st.session_state.personas_pool:
            st.caption(f"풀: {len(st.session_state.personas_pool)}명 ({st.session_state.personas_filename})")
            current_narratype = st.session_state.inputs_snapshot.get("context", "") or st.session_state.get("ctx_text_input", "")
            if st.button(L("ai_recommend_council"), use_container_width=True, key="council_recommend",
                         help="현재 narratype 입력을 기반으로 4명 자동 선정. 너무 적으면 narratype 입력 후 다시 시도."):
                if not current_narratype.strip():
                    st.warning("narratype 핵심 단락(맥락 입력)을 먼저 작성해주세요.")
                else:
                    with st.spinner("Council 구성 중... (Ollama)"):
                        try:
                            mapping = personas_mod.recommend_council(
                                narratype_text=current_narratype,
                                personas=st.session_state.personas_pool,
                                model=st.session_state.model or "gemma4",
                                n_candidates=min(30, len(st.session_state.personas_pool)),
                            )
                            council = {role: st.session_state.personas_pool[idx] for role, idx in mapping.items()}
                            st.session_state.council = council
                            st.session_state.council_mode = True
                            st.success("Council 구성 완료")
                        except Exception as e:
                            st.error(f"추천 실패: {e}")

            if st.session_state.council:
                st.markdown("**현재 Council:**")
                for role in ["scout", "critic", "director", "advisor"]:
                    p = st.session_state.council.get(role)
                    if p is not None:
                        label, _ = personas_mod.ROLE_DESCRIPTIONS.get(role, (role, ""))
                        st.markdown(f"- {label}: **{p.get('이름', '?')}** ({p.get('나이', '?')}세, {p.get('시도', '?')}, {p.get('직업', '?')[:14]})")

                council_on = st.checkbox(
                    L("council_mode_on"),
                    value=st.session_state.council_mode,
                    help="체크하면 거울/지도/의장/미래학자가 위 페르소나의 1인칭 목소리로 발언합니다.",
                )
                st.session_state.council_mode = council_on

                if st.button(L("council_reset"), key="council_reset", use_container_width=False):
                    st.session_state.council = {}
                    st.session_state.council_mode = False
                    st.rerun()

        st.markdown("---")

        # Council 라운드 수 — N-round iteration
        n_rounds_pick = st.slider(
            L("n_rounds_label"),
            min_value=1, max_value=5,
            value=st.session_state.get("n_rounds", 1),
            help="1 = 거울→지도→의장 단일 패스 (기본). "
                 "2~5 = 의장 결과가 다시 거울로 들어가 N회 반복 (수렴/심화). "
                 "라운드↑ → 응답 시간 N배 (로컬 Ollama라 비용 무료)."
        )
        st.session_state.n_rounds = n_rounds_pick

        st.markdown("---")

        # 미래학자 모드 토글
        advisor_on = st.checkbox(
            L("advisor_mode"),
            value=st.session_state.advisor_mode,
            help="파이프라인 말미에 '미래학자 하나'가 Dator 4 archetypes 메타 질문 10개를 생성합니다.",
        )
        st.session_state.advisor_mode = advisor_on

        # advisor 켜진 즉시 — 미래학자 전용 모델 선택 노출 (per_agent_mode 안 켜도 됨)
        if advisor_on and installed:
            adv_opts = [m[0] for m in installed_sorted]
            adv_default = st.session_state.agent_models.get("advisor", selected_model)
            adv_idx = adv_opts.index(adv_default) if adv_default in adv_opts else 0
            adv_picked = st.selectbox(
                L("advisor_model"),
                adv_opts,
                index=adv_idx,
                key="advisor_model_pick",
                help="미래학자 에이전트만 다른 모델로 돌리고 싶을 때 (예: 더 큰 reasoning 모델로 메타 질문 quality ↑). "
                     "기본값 = 메인 모델과 동일.",
            )
            st.session_state.agent_models["advisor"] = adv_picked

        # 사고 모드 토글 — qwen3/deepseek-r1/gemma4 의 thinking 기능 활성화
        think_on = st.checkbox(
            L("thinking_mode"),
            value=st.session_state.think_mode,
            help="모델의 내부 추론 과정(<think>)을 활성화. 깊은 반증·방법론 검토에 유리하지만 "
                 "속도가 2-5배 느려지고 예산이 부족하면 응답이 비어 나올 수 있습니다. "
                 "qwen3·deepseek-r1 같은 사고 계열 모델에서 특히 효과적.",
        )
        st.session_state.think_mode = think_on

        st.markdown("---")

        # 단계별 필수 항목 가이드
        st.markdown('<div class="section-label">단계별 필수 항목</div>', unsafe_allow_html=True)
        guide_stage = st.selectbox(
            "참고할 단계", RESEARCH_STAGES, key="guide_stage", label_visibility="collapsed"
        )
        if guide_stage in REQUIRED_ITEMS:
            for item in REQUIRED_ITEMS[guide_stage]:
                st.markdown(f"- {item}")

        st.markdown(
            '<div class="footer-note">'
            "Harness Engineering Demo<br>"
            "같은 하네스, 다른 프롬프트<br>"
            '<a href="https://www.youtube.com/watch?v=t7JjQTEnKOo" '
            'style="color:#8a8a8a">원본: 나만의 법무팀</a>'
            "</div>",
            unsafe_allow_html=True,
        )

    # ─────────────────────────────────────────────
    # 메인 영역 — Masthead
    # ─────────────────────────────────────────────
    st.markdown(
        """
        <div class="masthead">
            <div class="masthead-sub">Yonsei University · College of Human Ecology · 2026 Speculative Design</div>
            <div class="masthead-title">Speculative Design Council</div>
            <div class="masthead-desc">
                4-에이전트 Council × 3 단계 = narratype 분석 / AGENTS.md 작성 / 청중 반응. 로컬 LLM 기반, 데이터 외부 전송 없음.
            </div>
            <hr class="masthead-rule">
        </div>
        """,
        unsafe_allow_html=True,
    )

    # ─────────────────────────────────────────────
    # ONBOARDING — 3-step indicator + first-run guide
    # ─────────────────────────────────────────────
    has_inputs = bool(st.session_state.inputs_snapshot.get("context"))
    has_council = bool(st.session_state.get("council"))
    has_output = bool(st.session_state.get("director_output"))

    s1_label = "완료" if has_inputs else "필수"
    s2_label = "완료" if has_council else ("선택" if has_inputs else "대기")
    s3_label = "완료" if has_output else ("준비" if has_inputs else "대기")

    def _step_badge(label):
        color = {"완료": "#2d6a4f", "필수": "#9b2c2c", "선택": "#8b6914", "준비": "#2c5f7c", "대기": "#8a8a8a"}.get(label, "#8a8a8a")
        return f'<span style="display: inline-block; min-width: 38px; padding: 2px 8px; border-radius: 3px; background: {color}; color: white; font-size: 0.72rem; font-weight: 600; text-align: center; margin-right: 8px;">{label}</span>'

    st.markdown(
        f"""
        <div style="background: #f5f0e8; border-left: 4px solid #2c5f7c;
                    padding: 0.9rem 1.2rem; margin-bottom: 1.2rem; border-radius: 4px;
                    font-family: 'Noto Sans KR', sans-serif; font-size: 0.92rem; color: #1a1a1a; line-height: 1.85;">
            <div style="font-weight: 700; color: #1a3d52; margin-bottom: 0.6rem; font-size: 0.95rem;">
                사용 흐름 (처음이라면 여기부터)
            </div>
            <div>{_step_badge(s1_label)} <b>Step 1.</b> narratype 핵심 단락 작성 — 아래 '맥락' 입력란, 200-400자</div>
            <div>{_step_badge(s2_label)} <b>Step 2.</b> (선택) Persona Council 구성 — 사이드바에 Excel 업로드 → AI 추천 → Council 모드 ON</div>
            <div>{_step_badge(s3_label)} <b>Step 3.</b> [Council 실행] 버튼 클릭 — 거울→지도→의장 순차 진행 후 산출물 다운로드</div>
            <details style="margin-top: 0.6rem;">
                <summary style="cursor: pointer; color: #2c5f7c; font-size: 0.85rem; font-weight: 500;">용어 + 더 자세히 (펼치기)</summary>
                <div style="margin-top: 0.5rem; font-size: 0.85rem; color: #4a4a4a;">
                  <div style="background: #fff8e1; padding: 0.5rem 0.7rem; border-radius: 3px; margin-bottom: 0.5rem; border-left: 3px solid #8b6914;">
                    <b>왜 이렇게 디자인되었나? / Why this design?</b><br>
                    거울·지도·의장·미래학자, 4 archetype, Persona Council — 처음엔 헷갈릴 수 있습니다. 설계 의도는 <b>WHY.md</b> (repo 루트, 한·영 양국어) 참조. The design intent is in <b>WHY.md</b> at the repo root.
                  </div>
                  <div style="background: white; padding: 0.5rem 0.7rem; border-radius: 3px; margin-bottom: 0.5rem;">
                    <b>용어 안내</b><br>
                    • <b>narratype</b>: 본 수업의 핵심 작업 단위. 미래 시나리오 + 거주 인물 + 세계관의 결합 (narrative + archetype).<br>
                    • <b>Dator 4 archetypes</b>: 4가지 미래 원형 — 성장(Continued Growth) · 붕괴(Collapse) · 지속(Discipline) · 변혁(Transformation).<br>
                    • <b>AGENTS.md</b>: 2026 현재 Antigravity·Claude Code·Codex가 사용하는 협업 AI 표준 markdown 파일.<br>
                    • <b>Persona Council</b>: 추상적 거울/지도/의장 대신 Nemotron 페르소나 4명이 1인칭으로 Council 역할을 연기.
                  </div>
                  • <b>3단계 의미</b>:<br>
                  &nbsp;&nbsp;1. <b>Narratype 분석</b> — 본인 시나리오를 4 archetype으로 펼침<br>
                  &nbsp;&nbsp;2. <b>AGENTS.md 작성</b> — 시나리오 세계 AI 거버넌스 문서 자동 생성<br>
                  &nbsp;&nbsp;3. <b>청중 반응 시뮬레이션</b> — 페르소나 30명이 작품에 반응 + archetype 분포 분석<br>
                  • <b>산출물</b>: 실행 후 하단에 다운로드 — .docx 보고서 / AGENTS.md / Constellation 좌표 / 청중 반응 보고서.<br>
                  • <b>한 단계 재실행</b>: 결과가 마음에 안 들면 거울/지도/의장 중 하나만 다시 돌릴 수 있음.
                </div>
            </details>
        </div>
        """,
        unsafe_allow_html=True,
    )

    st.markdown(
        '<div class="disclaimer-box">'
        "본 도구의 출력은 AI가 생성한 초안이며 학생의 작가적 결정을 대체하지 않습니다. "
        "Persona Council 응답은 합성 페르소나 기반 시뮬레이션입니다 (실제 사람 의견 아님). "
        "업로드 파일은 로컬 메모리에만 보관되며 외부로 전송되지 않습니다."
        "</div>",
        unsafe_allow_html=True,
    )

    # ─────────────────────────────────────────────
    # 프로젝트명 + 빠른 시작 (4 데모 시나리오 중 선택)
    # ─────────────────────────────────────────────
    st.markdown('<div class="section-label">프로젝트</div>', unsafe_allow_html=True)
    pn_col, demo_pick_col, demo_btn_col = st.columns([3, 2, 1])
    with pn_col:
        project_name = st.text_input(
            "프로젝트 이름",
            value=st.session_state.project_name,
            placeholder=PROJECT_NAME_PLACEHOLDER,
            label_visibility="collapsed",
        )
    from templates import DEMO_SCENARIOS
    demo_keys = list(DEMO_SCENARIOS.keys())
    demo_labels = [DEMO_SCENARIOS[k]["label"] for k in demo_keys]
    with demo_pick_col:
        picked_demo = st.selectbox(
            "예시 시나리오",
            options=demo_keys,
            format_func=lambda k: DEMO_SCENARIOS[k]["label"],
            label_visibility="collapsed",
            key="demo_picker",
        )
    with demo_btn_col:
        if st.button(L("example_load"), help="선택한 2025 학생 narratype을 자동 입력합니다.", use_container_width=True):
            load_demo_scenario(picked_demo)
            st.rerun()
    st.session_state.project_name = project_name

    # ─────────────────────────────────────────────
    # 로컬 자료 업로더
    # ─────────────────────────────────────────────
    st.markdown('<div class="section-label">narratype 보조 자료 (선택 · PDF / MD / TXT)</div>', unsafe_allow_html=True)
    st.caption("⚠ Persona 풀 (Nemotron Excel) 은 여기가 아니라 **사이드바 → Council 구성** 에서 업로드하세요.")
    uploaded_files = st.file_uploader(
        RESOURCES_HELP,
        type=["pdf", "md", "txt"],
        accept_multiple_files=True,
        key="resource_uploader",
    )
    if uploaded_files:
        resources, errors = ingest_uploads(uploaded_files)
        st.session_state.resources = resources
        if errors:
            for err in errors:
                st.warning(err)
    if st.session_state.resources:
        def _human_size(text: str) -> str:
            n = len(text.encode("utf-8"))
            if n < 1024:
                return f"{n}B"
            return f"{n / 1024:.1f}KB"
        chips = "".join(
            f'<span class="resource-chip">{r["filename"]} ({_human_size(r.get("text") or "")})</span>'
            for r in st.session_state.resources
        )
        st.markdown(chips, unsafe_allow_html=True)
    else:
        st.caption("업로드된 자료가 없으면 에이전트는 일반 지식으로 답변합니다 (모두 [추측] 태깅).")

    # ─────────────────────────────────────────────
    # 연구 맥락 입력 폼
    # ─────────────────────────────────────────────
    st.markdown('<div class="section-label">연구 맥락 입력</div>', unsafe_allow_html=True)

    col1, col2 = st.columns(2)
    with col1:
        field = st.selectbox(
            "연구 분야",
            RESEARCH_FIELDS,
            index=(RESEARCH_FIELDS.index(st.session_state.inputs_snapshot.get("field"))
                   if st.session_state.inputs_snapshot.get("field") in RESEARCH_FIELDS else 0),
        )
        if field == "기타 (직접 입력)":
            field = st.text_input("연구 분야 직접 입력", value=st.session_state.inputs_snapshot.get("field", ""))
    with col2:
        current_stage = st.session_state.inputs_snapshot.get("stage", RESEARCH_STAGES[0])
        stage = st.selectbox(
            L("stage_label"),
            RESEARCH_STAGES,
            index=RESEARCH_STAGES.index(current_stage) if current_stage in RESEARCH_STAGES else 0,
            help="단계별로 4-에이전트 프롬프트가 자동 전환됩니다 (Harness Engineering: 같은 코드, 다른 프롬프트).",
        )

    # 단계 설명 + 기대 결과물 (사용자 혼란 방지)
    from templates import STAGE_DESCRIPTIONS, STAGE_DESCRIPTIONS_EN
    desc_src = STAGE_DESCRIPTIONS_EN if st.session_state.get("language") == "en" else STAGE_DESCRIPTIONS
    desc = desc_src.get(stage)
    if desc:
        st.markdown(
            f"""
            <div style="background:#f0efe9; border-left:3px solid #2c5f7c;
                        padding:0.6rem 1rem; margin: 0.4rem 0 1rem 0; border-radius:3px;
                        font-size: 0.85rem; line-height: 1.7;">
              <div><b>{L("stage_box_does")}</b> {desc["summary"]}</div>
              <div style="color:#4a4a4a; margin-top:0.3rem;"><b>{L("stage_box_input")}</b> {desc["input"]}</div>
              <div style="color:#4a4a4a;"><b>{L("stage_box_output")}</b> {desc["output"]}</div>
              <div style="color:#8a8a8a; font-style:italic; margin-top:0.3rem; font-size:0.82rem;">{L("stage_box_when")} {desc["use_case"]}</div>
            </div>
            """,
            unsafe_allow_html=True,
        )

    keywords = st.text_input(
        "관심 키워드 (쉼표로 구분)",
        value=st.session_state.inputs_snapshot.get("keywords", ""),
        placeholder=KEYWORDS_PLACEHOLDER,
    )
    context_input = st.text_area(
        "연구 맥락",
        value=st.session_state.inputs_snapshot.get("context", ""),
        height=140,
        placeholder=CONTEXT_PLACEHOLDER,
        help="소속, 학위 과정, 사용 가능한 데이터, 선호 방법론 등",
    )
    extra_input = st.text_area(
        "추가 조건 (선택)",
        value=st.session_state.inputs_snapshot.get("extra", ""),
        height=70,
        placeholder=EXTRA_PLACEHOLDER,
    )

    # 실행 버튼
    if st.button(L("council_run"), type="primary", use_container_width=True):
        if not is_connected:
            st.error("Ollama에 연결할 수 없습니다. 터미널에서 `ollama serve`를 실행하세요.")
        elif not keywords.strip() or not context_input.strip():
            st.error("키워드와 연구 맥락은 반드시 입력해야 합니다.")
        elif not project_name.strip():
            st.error("프로젝트 이름을 입력하세요 (세션 저장에 사용됩니다).")
        else:
            reset_pipeline_outputs()
            # N-Round: reset round counters
            st.session_state.current_round = 1
            st.session_state.round_history = []
            st.session_state.inputs_snapshot = {
                "field": field,
                "stage": stage,
                "keywords": keywords,
                "context": context_input,
                "extra": extra_input,
                "advisor_mode": st.session_state.advisor_mode,
            }
            st.session_state.step = 1
            st.rerun()

    # ─────────────────────────────────────────────
    # 파이프라인 실행 + 시각화
    # ─────────────────────────────────────────────
    step = st.session_state.step
    advisor_on = st.session_state.advisor_mode
    inputs = st.session_state.inputs_snapshot
    resources = st.session_state.resources

    st.markdown("---")
    # Pipeline header + round indicator (visible only when n_rounds > 1)
    _n_rounds = st.session_state.get("n_rounds", 1)
    _cur_round = st.session_state.get("current_round", 1)
    if _n_rounds > 1 and step > 0:
        round_indicator = f' · <span style="background:#1a3d52;color:white;padding:2px 10px;border-radius:3px;font-size:0.78rem;font-weight:600;">Round {_cur_round} / {_n_rounds}</span>'
    elif _n_rounds > 1:
        round_indicator = f' · <span style="color:#8a8a8a;font-size:0.78rem;">예정: {_n_rounds} 라운드 반복</span>'
    else:
        round_indicator = ""
    st.markdown(
        f'<div class="section-label">파이프라인 · {inputs.get("stage") or stage}{round_indicator}</div>',
        unsafe_allow_html=True,
    )
    render_pipeline(step, advisor_on)

    # N-Round history accumulator — show completed rounds so user sees Council building up
    _rh = st.session_state.get("round_history", [])
    if _rh:
        for prev in _rh:
            with st.expander(f"이전 라운드 {prev['round']} 결과 (요약)", expanded=False):
                st.markdown(f"**거울 (Round {prev['round']})**")
                st.markdown(prev.get("scout", "")[:500] + ("..." if len(prev.get("scout", "")) > 500 else ""))
                st.markdown(f"**지도 (Round {prev['round']})**")
                st.markdown(prev.get("critic", "")[:500] + ("..." if len(prev.get("critic", "")) > 500 else ""))
                st.markdown(f"**의장 (Round {prev['round']}) — 종합**")
                st.markdown(prev.get("director", ""))

    stage_in_use = inputs.get("stage") or stage
    current_model = selected_model

    # ── Step 1: 거울 (scout) ──
    if step == 1 and inputs:
        model_for_step = pick_model("scout", current_model)
        st.markdown(
            f'<div class="result-header">Step I — 거울 (탐색/합성/RQ후보) <span style="font-family:IBM Plex Mono,monospace;font-size:0.7rem;color:#8a8a8a;">· {model_for_step}</span></div>',
            unsafe_allow_html=True,
        )
        think_slot = st.empty() if st.session_state.think_mode else None
        placeholder = st.empty()
        try:
            output = run_streamed(
                stream_ollama(
                    model_for_step,
                    get_personified_prompt(stage_in_use, "scout"),
                    build_user_payload(inputs, resources),
                    think=st.session_state.think_mode,
                ),
                placeholder,
                think_slot,
            )
            st.session_state.scout_output = output
            st.session_state.step = 2
            st.rerun()
        except Exception as e:
            st.error(f"오류: {e}")
            st.session_state.step = 0

    if step >= 2:
        with st.expander("Step I 결과 — 거울", expanded=False):
            st.markdown(st.session_state.scout_output)
            render_ledger(st.session_state.scout_output)

    # ── Step 2: 지도 (critic) ──
    if step == 2 and inputs:
        model_for_step = pick_model("critic", current_model)
        st.markdown(
            f'<div class="result-header">Step II — 지도 (검증) <span style="font-family:IBM Plex Mono,monospace;font-size:0.7rem;color:#8a8a8a;">· {model_for_step}</span></div>',
            unsafe_allow_html=True,
        )
        think_slot = st.empty() if st.session_state.think_mode else None
        placeholder = st.empty()
        try:
            output = run_streamed(
                stream_ollama(
                    model_for_step,
                    get_personified_prompt(stage_in_use, "critic"),
                    build_critic_payload(inputs, resources, st.session_state.scout_output),
                    think=st.session_state.think_mode,
                ),
                placeholder,
                think_slot,
            )
            st.session_state.critic_output = output
            st.session_state.step = 3
            st.rerun()
        except Exception as e:
            st.error(f"오류: {e}")
            st.session_state.step = 0

    if step >= 3:
        with st.expander("Step II 결과 — 지도", expanded=False):
            st.markdown(st.session_state.critic_output)
            render_ledger(st.session_state.critic_output)

    # ── Step 3: 의장 (director) ──
    if step == 3 and inputs:
        model_for_step = pick_model("director", current_model)
        st.markdown(
            f'<div class="result-header">Step III — 의장 (총괄) <span style="font-family:IBM Plex Mono,monospace;font-size:0.7rem;color:#8a8a8a;">· {model_for_step}</span></div>',
            unsafe_allow_html=True,
        )
        think_slot = st.empty() if st.session_state.think_mode else None
        placeholder = st.empty()
        try:
            output = run_streamed(
                stream_ollama(
                    model_for_step,
                    get_personified_prompt(stage_in_use, "director"),
                    build_director_payload(inputs, resources, st.session_state.scout_output, st.session_state.critic_output),
                    think=st.session_state.think_mode,
                ),
                placeholder,
                think_slot,
            )
            st.session_state.director_output = output
            # N-Round: record this round's outputs, decide if more rounds needed
            n_rounds = st.session_state.get("n_rounds", 1)
            cur = st.session_state.get("current_round", 1)
            st.session_state.round_history = st.session_state.get("round_history", []) + [{
                "round": cur,
                "scout": st.session_state.scout_output,
                "critic": st.session_state.critic_output,
                "director": output,
            }]
            if cur < n_rounds:
                # Next round: reset to step 1, increment round counter
                st.session_state.current_round = cur + 1
                st.session_state.scout_output = ""
                st.session_state.critic_output = ""
                # director_output kept for prior_block injection in build_user_payload
                st.session_state.step = 1
                st.rerun()
            else:
                # Final round complete → proceed to advisor or done
                st.session_state.step = 4 if advisor_on else 5
                if not advisor_on:
                    persist_current_version(f"파이프라인 {n_rounds}라운드 완료")
                st.rerun()
        except Exception as e:
            st.error(f"오류: {e}")
            st.session_state.step = 0

    if step >= 4:
        with st.expander("Step III 결과 — 의장", expanded=(step == 5)):
            st.markdown(st.session_state.director_output)
            render_ledger(st.session_state.director_output)

    # ── Step 4: 하나 (advisor, optional) ──
    if step == 4 and inputs and advisor_on:
        model_for_step = pick_model("advisor", current_model)
        st.markdown(
            f'<div class="result-header">Step IV — 하나 (미래학자) <span style="font-family:IBM Plex Mono,monospace;font-size:0.7rem;color:#8a8a8a;">· {model_for_step}</span></div>',
            unsafe_allow_html=True,
        )
        think_slot = st.empty() if st.session_state.think_mode else None
        placeholder = st.empty()
        try:
            output = run_streamed(
                stream_ollama(
                    model_for_step,
                    get_personified_advisor_prompt(),
                    build_advisor_payload(inputs, st.session_state.director_output),
                    think=st.session_state.think_mode,
                ),
                placeholder,
                think_slot,
            )
            st.session_state.advisor_output = output
            st.session_state.step = 5
            persist_current_version("파이프라인 v1 + 미래학자 모드 완료")
            st.rerun()
        except Exception as e:
            st.error(f"오류: {e}")
            st.session_state.step = 5

    if step >= 5 and advisor_on and st.session_state.advisor_output:
        with st.expander("Step IV 결과 — 하나 (미래학자)", expanded=True):
            st.markdown(st.session_state.advisor_output)
            render_ledger(st.session_state.advisor_output)

    # ─────────────────────────────────────────────
    # A/B 대조 실행 — 자료 없이 동일 파이프라인 재실행
    # ─────────────────────────────────────────────
    ab_step = st.session_state.ab_step
    if ab_step in (1, 2, 3) and inputs:
        ab_role = {1: "scout", 2: "critic", 3: "director"}[ab_step]
        role_label = {1: "거울 (탐색)", 2: "지도 (검증)", 3: "의장 (총괄)"}[ab_step]
        model_for_step = pick_model(ab_role, current_model)
        st.markdown(
            f'<div class="result-header">A/B 대조 — {role_label} · 자료 없이 실행 중… <span style="font-family:IBM Plex Mono,monospace;font-size:0.7rem;color:#8a8a8a;">· {model_for_step}</span></div>',
            unsafe_allow_html=True,
        )
        think_slot = st.empty() if st.session_state.think_mode else None
        placeholder = st.empty()
        try:
            if ab_step == 1:
                system = get_personified_prompt(stage_in_use, "scout")
                user = build_user_payload(inputs, [])
            elif ab_step == 2:
                system = get_personified_prompt(stage_in_use, "critic")
                user = build_critic_payload(inputs, [], st.session_state.ab_scout_output)
            else:
                system = get_personified_prompt(stage_in_use, "director")
                user = build_director_payload(inputs, [], st.session_state.ab_scout_output, st.session_state.ab_critic_output)
            out = run_streamed(
                stream_ollama(model_for_step, system, user, think=st.session_state.think_mode),
                placeholder, think_slot,
            )
            target = f"ab_{ab_role}_output"
            st.session_state[target] = out
            st.session_state.ab_step = ab_step + 1 if ab_step < 3 else 4
            st.rerun()
        except Exception as e:
            st.error(f"A/B {role_label} 오류: {e}")
            st.session_state.ab_step = 0

    # ─────────────────────────────────────────────
    # 완료 시: 배너 · v1↔v2 비교 · 정제 대화 · 산출물 메뉴
    # ─────────────────────────────────────────────
    if step == 5:
        render_completion(inputs, current_model)


# ═════════════════════════════════════════════════════════════════════
# 완료 화면 분리
# ═════════════════════════════════════════════════════════════════════

def render_completion(inputs: dict, model: str) -> None:
    state = st.session_state.session_state_dict or {}
    versions = state.get("versions", [])

    st.markdown(
        '<div class="completion-banner">'
        '<div class="completion-banner-title">파이프라인 완료 · 세션 저장됨</div>'
        '<div class="completion-banner-desc">'
        f".sessions/ 에 프로젝트가 저장되었습니다 (v{len(versions)}). "
        "아래에서 정제 대화·산출물을 이어가세요. 탭에서 v1/v2 비교 가능."
        "</div></div>",
        unsafe_allow_html=True,
    )

    # v1↔v2 비교 탭
    if len(versions) >= 2:
        latest2 = two_latest(state)
        tabs = st.tabs([f"v{v['version']} — {v['ts'][:16]}" for v in latest2])
        for tab, v in zip(tabs, latest2):
            with tab:
                if v.get("note"):
                    st.caption(v["note"])
                st.markdown("### 의장 (총괄)")
                st.markdown(v["outputs"].get("director", "") or "_(없음)_")
                if v["outputs"].get("advisor"):
                    st.markdown("### 하나 (미래학자)")
                    st.markdown(v["outputs"]["advisor"])

    # A/B 대조: 자료 포함 vs 자료 없음
    has_resources = bool(st.session_state.resources)
    ab_done = st.session_state.ab_step == 4 and st.session_state.ab_director_output
    ab_running = st.session_state.ab_step in (1, 2, 3)
    if has_resources and not ab_done and not ab_running:
        st.markdown(
            '<div class="result-header">A/B 대조 실행 (자료 효과 검증)</div>',
            unsafe_allow_html=True,
        )
        st.caption(
            "⚠️ 업로드 자료를 **빼고** 동일 파이프라인을 한 번 더 돌려 차이를 비교합니다. "
            "Track A '맥락(자료)의 효과'를 시각적으로 확인할 수 있습니다. "
            "약 3-6분 추가 소요."
        )
        if st.button("🅰🅱 자료 없이 재실행", key="ab_run_btn"):
            st.session_state.ab_step = 1
            st.rerun()
    elif ab_done:
        st.markdown(
            '<div class="result-header">A/B 대조 결과 — 자료 포함 vs 자료 없음</div>',
            unsafe_allow_html=True,
        )
        ab_tabs = st.tabs(["자료 포함 (원본)", "🅱 자료 없음 (대조)"])
        with ab_tabs[0]:
            ledger_with = count_grounding(st.session_state.director_output)
            st.caption(f"근거 {ledger_with['grounded_total']}건 / 추측 {ledger_with['speculated_total']}건")
            st.markdown(st.session_state.director_output)
        with ab_tabs[1]:
            ledger_without = count_grounding(st.session_state.ab_director_output)
            st.caption(f"근거 {ledger_without['grounded_total']}건 / 추측 {ledger_without['speculated_total']}건")
            st.markdown(st.session_state.ab_director_output)
        st.caption(
            "추측 태그 수가 자료 없는 쪽에서 눈에 띄게 늘고, 구체적 수치·근거가 줄어드는 것을 확인해보세요."
        )

    # 정제 대화 블록
    st.markdown('<div class="result-header">정제 대화 — 특정 단계만 재실행</div>', unsafe_allow_html=True)
    st.caption("예: '지도, 실행 가능성을 6개월 기준으로 재비판' → Step II 만 재실행, 버전 증가.")

    c1, c2 = st.columns([1, 3])
    with c1:
        target_label = st.radio(
            "대상 에이전트",
            options=[ROLE_LABELS["scout"], ROLE_LABELS["critic"], ROLE_LABELS["director"]]
                    + ([ROLE_LABELS["advisor"]] if st.session_state.advisor_mode else []),
            label_visibility="collapsed",
            key="refine_target_radio",
        )
    with c2:
        feedback = st.text_area(
            "보완 요청",
            placeholder="이 에이전트에게 어떤 식으로 다시 해달라고 할지 구체적으로 적으세요.",
            key="refine_feedback_area",
            height=100,
            label_visibility="collapsed",
        )
    if st.button("해당 단계만 재실행", type="primary"):
        target = {v: k for k, v in ROLE_LABELS.items()}.get(target_label, "critic")
        if feedback.strip():
            # Use the per-agent model for the selected role if advanced mode is on
            refine_model = pick_model(target, model)
            run_refinement(target, feedback, inputs, refine_model)
        else:
            st.warning("보완 요청 내용을 입력하세요.")

    # 산출물 메뉴
    st.markdown('<div class="result-header">산출물 내보내기</div>', unsafe_allow_html=True)
    render_exports(model)

    # Harness note
    if st.session_state.per_agent_mode and st.session_state.agent_models:
        split = " / ".join(
            f"<b>{r}</b>={m}" for r, m in st.session_state.agent_models.items() if m
        )
        harness_body = (
            f"현재 단계 ({inputs.get('stage')}) × 3개 역할 트리오가 활성화되었고, "
            f"역할마다 다른 모델이 할당되었습니다: {split}. "
            "같은 파이프라인 코드가 프롬프트(단계별)와 모델(역할별) 두 축으로 재사용됩니다. "
            "이것이 Harness Engineering 의 두 번째 증거입니다."
        )
    else:
        harness_body = (
            f"현재 단계 ({inputs.get('stage')}) × 3개 역할 트리오가 활성화되었습니다. "
            "단계 드롭다운을 바꾸면 동일한 3-에이전트 코드가 다른 프롬프트 트리오로 재사용됩니다. "
            "이것이 '같은 하네스, 다른 프롬프트'의 실체입니다. "
            "사이드바의 '️ 에이전트별 모델 지정'을 켜면 역할별 모델 축도 추가됩니다."
        )
    st.markdown(
        '<div class="harness-note">'
        '<div class="harness-note-title">Harness Engineering</div>'
        f'<div class="harness-note-text">{harness_body}</div></div>',
        unsafe_allow_html=True,
    )


# ═════════════════════════════════════════════════════════════════════
# 정제 실행 (해당 단계만 재실행 + 버전 append)
# ═════════════════════════════════════════════════════════════════════

def run_refinement(role: str, feedback: str, inputs: dict, model: str) -> None:
    stage_in_use = inputs.get("stage") or RESEARCH_STAGES[0]
    resources = st.session_state.resources

    # 기존 해당 역할 출력 + 피드백을 user payload에 붙임
    feedback_block = (
        f"=== 사용자 보완 요청 ===\n{feedback}\n=== 요청 끝 ===\n\n"
        f"이 요청을 반드시 반영하여 해당 역할 결과물을 재작성하세요."
    )

    if role == "scout":
        system = get_personified_prompt(stage_in_use, "scout")
        user = build_user_payload(inputs, resources) + "\n\n" + feedback_block
        target_key = "scout_output"
    elif role == "critic":
        system = get_personified_prompt(stage_in_use, "critic")
        user = build_critic_payload(inputs, resources, st.session_state.scout_output) + "\n\n" + feedback_block
        target_key = "critic_output"
    elif role == "director":
        system = get_personified_prompt(stage_in_use, "director")
        user = build_director_payload(inputs, resources, st.session_state.scout_output, st.session_state.critic_output) + "\n\n" + feedback_block
        target_key = "director_output"
    elif role == "advisor":
        system = get_personified_advisor_prompt()
        user = build_advisor_payload(inputs, st.session_state.director_output) + "\n\n" + feedback_block
        target_key = "advisor_output"
    else:
        st.error(f"알 수 없는 역할: {role}")
        return

    st.markdown(f'<div class="result-header">정제 실행 — {ROLE_LABELS.get(role, role)}</div>', unsafe_allow_html=True)
    think_slot = st.empty() if st.session_state.think_mode else None
    placeholder = st.empty()
    try:
        output = run_streamed(
            stream_ollama(model, system, user, think=st.session_state.think_mode),
            placeholder,
            think_slot,
        )
        st.session_state[target_key] = output
        persist_current_version(f"정제 v{_next_version_num()}: {role} — {feedback[:40]}")
        st.success(f"{ROLE_LABELS.get(role, role)} 재실행 완료. 버전이 추가되었습니다.")
        st.rerun()
    except Exception as e:
        st.error(f"정제 실행 오류: {e}")


def _next_version_num() -> int:
    state = st.session_state.session_state_dict or {}
    return len(state.get("versions", [])) + 1


# ═════════════════════════════════════════════════════════════════════
# 산출물 메뉴
# ═════════════════════════════════════════════════════════════════════

def render_exports(model: str) -> None:
    director_output = st.session_state.director_output
    advisor_output = st.session_state.advisor_output

    if not director_output:
        st.info("의장 (총괄) 결과가 없으면 내보내기를 생성할 수 없습니다.")
        return

    choice = st.radio(
        "포맷 선택",
        options=list(EXPORT_LABELS.keys()),
        format_func=lambda k: EXPORT_LABELS[k],
        horizontal=False,
        key="export_radio",
    )

    if st.button("산출물 생성", key="export_btn"):
        reg = EXPORT_REGISTRY[choice]
        stamp = datetime.datetime.now().strftime("%Y%m%d_%H%M")
        filename = f"{reg['filename']}_{stamp}.{reg['ext']}"

        if reg["kind"] == "docx":
            final_text = extract_final_doc(director_output) or director_output
            buf = create_docx(final_text, DOCX_HEADER, DOCX_DISCLAIMER)
            st.download_button(
                label=f"⬇ {filename} 내려받기",
                data=buf,
                file_name=filename,
                mime=reg["mime"],
                type="primary",
            )
        else:
            fn = reg["fn"]
            with st.spinner(f"{EXPORT_LABELS[choice]} 생성 중... (로컬 Ollama)"):
                # agents_md takes optional student_name as 3rd arg; others take just director_output
                if choice == "agents_md":
                    content = fn(model, director_output, st.session_state.get("project_name", "학생"))
                else:
                    content = fn(model, director_output)
            st.text_area("생성된 산출물 미리보기", value=content, height=260)
            st.download_button(
                label=f"⬇ {filename} 내려받기",
                data=content.encode("utf-8"),
                file_name=filename,
                mime=reg["mime"],
                type="primary",
            )


if __name__ == "__main__":
    main()
