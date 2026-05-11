# Conversion Log — research_team → spec_design_council

## 출처
- 원본: `~/demo/streamlit_research_team` (HarmonyOn / Yonsei 0424 research workshop)
- 변환일: 2026.05.11
- 목적: Yonsei Speculative Design 2026 워크숍의 Hook 도구 + 학생 자율 활용 도구

## 변경 사항 요약

### 도메인 변환
| 영역 | 원본 (research_team) | 변환 (spec_design_council) |
|---|---|---|
| 도메인 | 대학원 연구 설계 | Speculative Design 시나리오 확장 |
| 입력 분야 | 식품영양/노화과학/디자인 등 | 감정·정서 / 노동·일상 / 신체·웨어러블 등 |
| 단계 1 | 주제 탐색 | **Narratype 분석** (4 archetype lens) |
| 단계 2 | 선행연구 정리 | **AGENTS.md 작성** (실제 markdown 표준) |
| 단계 3 | RQ 도출 | **청중 반응 시뮬레이션** (Nemotron 페르소나) |

### 에이전트 이름 변경
| 원본 | 변환 |
|---|---|
| 수연 (Scout) | 🪞 거울 (Mirror) |
| 준호 (Critic) | 📍 지도 (Map) |
| 지은 (Director) | ⚖️ 의장 (Chairman) |
| 한민수 지도교수 (Advisor) | 🔮 미래학자 — 하나 (Dator 4 archetypes lens) |

### Export 형식 변경
| 원본 | 변환 |
|---|---|
| 지도교수 회의 1-pager (.md) | **AGENTS.md** (.md) — narratype 세계 protocol |
| RISS/NTIS/Scholar 검색 쿼리 (.txt) | **Constellation 좌표** (.txt) — STEEP 휠 + 4 archetype |
| IRB 체크카드 (.md) | **Living Diptych 시드** (.md) — Alt 1 우측 패널 초기값 |
| BibTeX seed (.bib) | **청중 반응 보고서** (.md) — 페르소나 분석 |

### 유지된 부분 (변환 없음)
- Streamlit UI 코드 + CSS 스타일링
- Ollama 호출 로직 (`_ollama_once`, streaming)
- 세션 영속성 (`.sessions/*.json`)
- 파일 grounding (PDF/md/txt 업로드 + `[근거:파일]` 태깅)
- Per-agent 모델 선택
- Thinking mode 토글
- Harness Engineering 메시지 ("같은 코드, 다른 프롬프트")

## 변환 작업 순서
1. 폴더 fork → SD_2026_05/streamlit_spec_design_council/
2. `agents.py` 전면 재작성 (12 prompts: 3 stages × 3 roles + 1 advisor + Dator lens)
3. `templates.py` 전면 재작성 (input fields, placeholders, export labels)
4. `exporters.py` 전면 재작성 (4 SD-domain exporters + create_docx 유지)
5. `app.py` 부분 수정 (sed 일괄: 에이전트 이름 + 도메인 용어)
6. `smoke_test.py` 재작성 (SD-specific 구조 검증, 58 checks)
7. `README.md` + `DEMO_SCRIPT_SD.md` 신규 작성

## 정합성 검증
```bash
python smoke_test.py
# 58 PASSED, 0 FAILED
```

검증 항목:
- 모듈 임포트 (5개)
- 프롬프트 스왑 (3 stages × 3 roles + advisor = 10 검증)
- Grounding rule 주입 (9개)
- get_prompt round-trip + defensive fallback
- Role labels 한국어 (4개)
- 템플릿 / 스테이지 일관성 (6개)
- Export 레지스트리 일관성 (13개)
- 세션 영속성 round-trip (1개)
- 데모 시나리오 (3개)

## 알려진 제약
- 원본 `DEMO_SCENARIOS.md` / `GUIDE.md` / `PROMPTS.md` 는 보존되지 않음 (도메인 차이 너무 큼)
- 학생들이 GitHub에서 클론 후 직접 실행 가능하도록 의도 (워크숍 후 자율 사용)
- MTP drafter (`gemma4-mtp`) 권장 — 워크숍 라이브 시연 시 응답 속도 3x 가속

## Option D 추가 (Persona Council)
- 신규 모듈: `personas.py` (~280 lines) — Nemotron-Personas-Korea 로드 + AI 추천 + prompt 주입
- app.py 사이드바에 "Council 구성" UI 추가 (파일 업로더 + AI 추천 + 4명 표시 + 토글)
- 핵심 함수 `make_personified_prompt(role, base_prompt, persona)` — backward compatible (persona=None → 기존 동작)
- agent.py STAGE_PROMPTS / ADVISOR_PROMPT 전혀 변경 없음 — Harness Engineering 메시지 강화 (페르소나도 "다른 프롬프트"의 일부)
- smoke test 13개 추가 (총 71/71 통과)

학생 결정 흐름:
1. 페르소나 파일 안 올림 → 기존 추상 Council (모드 A)
2. 파일 올림 + Council 모드 OFF → 추상 Council 유지 (페르소나는 옵션)
3. 파일 올림 + AI 추천 + Council 모드 ON → Persona Council (모드 B): 4명이 거울/지도/의장/미래학자 역할을 1인칭으로 연기

## 원본 변경 사항 추적
원본 코드의 다음 함수들은 **재구현이 아니라 prompt만 교체**:
- `_ollama_once` (그대로)
- `create_docx` (그대로, 헤더만 templates.DOCX_HEADER 통해 SD 톤)
- `STAGE_PROMPTS` dict 구조 (그대로, 내용만 교체)
- `EXPORT_REGISTRY` dict 구조 (그대로, 내용만 교체)

이로써 **Harness Engineering 메시지** ("같은 코드, 다른 프롬프트로 도메인 전환")가 코드 자체로 증명됨.
