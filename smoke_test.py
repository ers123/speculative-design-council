#!/usr/bin/env python3
"""Speculative Design Council — 스모크 테스트 (구조 정합성 검증).

Ollama·Streamlit 서버 없이 구조 정합성만 확인:
  1. 핵심 모듈 임포트
  2. 프롬프트 스왑 로직 (3 stages × 3 roles = 9개 + 1 advisor)
  3. 템플릿 / 스테이지 일관성 (agents.STAGE_PROMPTS keys == templates.RESEARCH_STAGES)
  4. 산출물 레지스트리 일관성 (EXPORT_REGISTRY ↔ EXPORT_LABELS)
  5. 세션 영속성 round-trip (JSON 저장/복원)
  6. 데모 시나리오 입력 검증

사용:
    python smoke_test.py

종료 코드:
    0  — 전부 통과
    1+ — 실패 개수
"""

from __future__ import annotations

import json
import os
import sys
import tempfile
from pathlib import Path


PASSED = 0
FAILED = 0
FAILURES: list[str] = []


def check(label: str, cond: bool, detail: str = "") -> None:
    global PASSED, FAILED
    status = "PASS" if cond else "FAIL"
    print(f"  [{status}] {label}" + (f"  — {detail}" if detail else ""))
    if cond:
        PASSED += 1
    else:
        FAILED += 1
        FAILURES.append(f"{label} — {detail}")


def section(title: str) -> None:
    print(f"\n── {title} ──")


def main() -> int:
    here = Path(__file__).parent
    print("=" * 60)
    print("  Speculative Design Council — Smoke Test")
    print("=" * 60)

    # 1. 모듈 임포트
    section("1. 핵심 모듈 임포트")
    try:
        import agents
        check("agents.py import", True)
    except Exception as e:
        check("agents.py import", False, str(e))
        return 1
    try:
        import templates
        check("templates.py import", True)
    except Exception as e:
        check("templates.py import", False, str(e))
    try:
        import resources
        check("resources.py import", True)
    except Exception as e:
        check("resources.py import", False, str(e))
    try:
        import sessions
        check("sessions.py import", True)
    except Exception as e:
        check("sessions.py import", False, str(e))
    try:
        import exporters
        check("exporters.py import", True)
    except Exception as e:
        check("exporters.py import", False, str(e))

    from agents import STAGE_PROMPTS, ADVISOR_PROMPT, ROLE_LABELS, ROLE_EMOJI, AGENTS, get_prompt

    # 2. 프롬프트 스왑 (3 stages × 3 roles = 9)
    section("2. 프롬프트 스왑 (3 stages × 3 roles = 9)")
    expected_stages = ["Narratype 분석", "AGENTS.md 작성", "청중 반응 시뮬레이션"]
    for stage in expected_stages:
        check(f"STAGE_PROMPTS has '{stage}'", stage in STAGE_PROMPTS)

    for stage in expected_stages:
        if stage not in STAGE_PROMPTS:
            continue
        for role in ["scout", "critic", "director"]:
            try:
                p = STAGE_PROMPTS[stage][role]
                check(f"  {stage} / {role} prompt non-empty",
                      isinstance(p, str) and len(p) > 100, f"len={len(p)}")
            except KeyError:
                check(f"  {stage} / {role} prompt non-empty", False, "KeyError")

    # Grounding rule injected
    for stage in expected_stages:
        if stage not in STAGE_PROMPTS:
            continue
        for role in ["scout", "critic", "director"]:
            p = STAGE_PROMPTS[stage].get(role, "")
            check(f"  {stage} / {role} contains grounding rule",
                  "근거 태깅 규칙" in p)

    # get_prompt round-trip (note: get_prompt appends language directive, so use startswith)
    check("get_prompt('Narratype 분석', 'scout') starts with STAGE_PROMPTS prompt",
          get_prompt("Narratype 분석", "scout").startswith(STAGE_PROMPTS["Narratype 분석"]["scout"]))

    # Defensive fallback
    fb = get_prompt("unknown_stage", "scout")
    expected_prefix = STAGE_PROMPTS[next(iter(STAGE_PROMPTS))]["scout"]
    check("get_prompt('unknown_stage', 'scout') falls back to first stage", fb.startswith(expected_prefix))

    # Language directive injection
    en_prompt = get_prompt("Narratype 분석", "scout", language="en")
    check("get_prompt(language='en') includes English directive",
          "OUTPUT LANGUAGE: ENGLISH" in en_prompt)
    ko_prompt = get_prompt("Narratype 분석", "scout", language="ko")
    check("get_prompt(language='ko') includes Korean directive",
          "출력 언어: 한국어" in ko_prompt)

    # Advisor prompt
    check("ADVISOR_PROMPT non-empty + has Dator lens",
          len(ADVISOR_PROMPT) > 200 and "Dator" in ADVISOR_PROMPT)

    # Role labels
    expected_roles = {"scout", "critic", "director", "advisor"}
    check("ROLE_LABELS has 4 roles", set(ROLE_LABELS.keys()) == expected_roles)
    check("ROLE_EMOJI has 4 roles", set(ROLE_EMOJI.keys()) == expected_roles)
    check("AGENTS dict has 4 roles", set(AGENTS.keys()) == expected_roles)

    # Korean names
    check("scout label is 거울 (Mirror)", "거울" in ROLE_LABELS["scout"])
    check("critic label is 지도 (Map)", "지도" in ROLE_LABELS["critic"])
    check("director label is 의장 (Chairman)", "의장" in ROLE_LABELS["director"])
    check("advisor label is 미래학자 (Futurist)", "미래학자" in ROLE_LABELS["advisor"])

    # 3. 템플릿 / 스테이지 일관성
    section("3. 템플릿 / 스테이지 일관성")
    check("templates.RESEARCH_STAGES == STAGE_PROMPTS keys",
          set(templates.RESEARCH_STAGES) == set(STAGE_PROMPTS.keys()))
    check("templates.NARRATYPE_DOMAINS non-empty", len(templates.NARRATYPE_DOMAINS) > 0)
    check("templates.RESEARCH_FIELDS aliases NARRATYPE_DOMAINS",
          templates.RESEARCH_FIELDS == templates.NARRATYPE_DOMAINS)
    check("templates.REQUIRED_ITEMS covers all stages",
          set(templates.REQUIRED_ITEMS.keys()) == set(STAGE_PROMPTS.keys()))
    check("templates.DEMO_INPUTS has expected keys",
          set(["field", "stage", "context", "keywords", "extra"]).issubset(set(templates.DEMO_INPUTS.keys())))
    check("DEMO_INPUTS.stage is valid",
          templates.DEMO_INPUTS["stage"] in STAGE_PROMPTS)

    # 4. 산출물 레지스트리 일관성
    section("4. 산출물 레지스트리 (EXPORT_REGISTRY / EXPORT_LABELS) 일관성")
    expected_exports = ["docx", "agents_md", "constellation", "diptych_seed", "audience_report"]
    check("EXPORT_REGISTRY has 5 keys", set(exporters.EXPORT_REGISTRY.keys()) == set(expected_exports))
    check("EXPORT_LABELS has 5 keys", set(templates.EXPORT_LABELS.keys()) == set(expected_exports))
    check("EXPORT_REGISTRY keys == EXPORT_LABELS keys",
          set(exporters.EXPORT_REGISTRY.keys()) == set(templates.EXPORT_LABELS.keys()))

    for k, reg in exporters.EXPORT_REGISTRY.items():
        check(f"  EXPORT_REGISTRY['{k}'] has all required fields",
              all(f in reg for f in ["label", "filename", "ext", "mime", "kind"]))
        if reg["kind"] == "llm":
            check(f"  EXPORT_REGISTRY['{k}'] has callable fn",
                  callable(reg.get("fn")))

    # 5. 세션 영속성 round-trip
    section("5. 세션 영속성 round-trip")
    try:
        entry = sessions.new_version_entry(
            stage="Narratype 분석",
            model="gemma4",
            outputs={"scout": "s", "critic": "c", "director": "d"},
            note="smoke test",
        )
        state = {"versions": [], "current_inputs": {}}
        sessions.append_version(state, entry)
        path = sessions.save_session("smoke_test_session", state)
        loaded = sessions.load_session(path)
        check("save_session + load_session round-trip",
              loaded.get("versions", [{}])[0].get("stage") == "Narratype 분석")
        # cleanup
        try:
            from pathlib import Path as _P
            _P(path).unlink(missing_ok=True)
        except Exception:
            pass
    except Exception as e:
        check("session round-trip", False, str(e))

    # 6a. 페르소나 Council (Option D) 모듈 정합성
    section("6a. personas.py (Option D) 구조 정합성")
    try:
        import personas as personas_mod
        check("personas.py import", True)
    except Exception as e:
        check("personas.py import", False, str(e))
        personas_mod = None

    if personas_mod is not None:
        check("personas.load_personas exists", callable(getattr(personas_mod, "load_personas", None)))
        check("personas.recommend_council exists", callable(getattr(personas_mod, "recommend_council", None)))
        check("personas.make_personified_prompt exists", callable(getattr(personas_mod, "make_personified_prompt", None)))
        check("personas.format_persona_brief exists", callable(getattr(personas_mod, "format_persona_brief", None)))
        check("personas.ROLE_DESCRIPTIONS has 4 roles",
              set(personas_mod.ROLE_DESCRIPTIONS.keys()) == {"scout", "critic", "director", "advisor"})

        # Test format with synthetic persona
        sample = {"이름": "전기태", "나이": 74, "성별": "남자", "시도": "광주",
                  "시군구": "광주-서구", "직업": "하역 종사원", "학력": "초등학교",
                  "한줄_persona": "광주 서구에서 평생 하역 일을 하며 살아온 70대 가장",
                  "문화배경": "투박한 전라도 사투리", "취미": "무등산 산책"}
        brief = personas_mod.format_persona_brief(sample)
        check("format_persona_brief includes name", "전기태" in brief)
        check("format_persona_brief includes region", "광주" in brief)

        # Backward compat: no persona = passthrough
        base = "test base prompt"
        result = personas_mod.make_personified_prompt("scout", base, None)
        check("make_personified_prompt(persona=None) returns base unchanged", result == base)

        # With persona: should contain identity markers + base
        result_with = personas_mod.make_personified_prompt("scout", base, sample)
        check("make_personified_prompt with persona contains 전기태", "전기태" in result_with)
        check("make_personified_prompt with persona contains base prompt", base in result_with)
        check("make_personified_prompt has 1인칭 instruction",
              "1인칭" in result_with or "자기소개로 시작" in result_with)

        # Council summary
        council = {"scout": sample, "critic": sample, "director": sample, "advisor": sample}
        summary = personas_mod.council_summary_md(council)
        check("council_summary_md mentions all 4 roles",
              all(label in summary for label, _ in personas_mod.ROLE_DESCRIPTIONS.values()))

    # 6. 데모 시나리오 입력 검증
    section("6. 데모 시나리오 입력")
    check("DEMO_PROJECT_NAME set", bool(templates.DEMO_PROJECT_NAME))
    check("DEMO_INPUTS.context references HAPPY GATE example",
          "HAPPY GATE" in templates.DEMO_INPUTS.get("context", ""))
    check("DOCX_HEADER mentions Council or Speculative Design",
          "Council" in templates.DOCX_HEADER or "Speculative Design" in templates.DOCX_HEADER)

    # ── Summary ──
    print()
    print("=" * 60)
    print(f"  Result: {PASSED} PASSED, {FAILED} FAILED")
    print("=" * 60)
    if FAILURES:
        print("\nFailures:")
        for f in FAILURES:
            print(f"  - {f}")
    return FAILED


if __name__ == "__main__":
    sys.exit(main())
