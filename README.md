# Speculative Design Council

Local AI tool for the Yonsei University 2026 Speculative Design class.
A 4-agent council (Mirror / Map / Chairman / Futurist) deliberates on student narratypes using Ollama + Gemma 4, fully offline.

연세대 2026 Speculative Design 수업 보조 도구. 4명의 AI 에이전트(거울/지도/의장/미래학자)가 학생의 narratype을 분석·확장합니다. Ollama + Gemma 4 기반, 완전 오프라인 작동.

> **🎓 학생 여러분께 / For students** — 이 도구의 설치는 **선택사항**입니다. 수업 당일 직접 시연하니, 그냥 보고 따라와도 됩니다. 워크숍 필수 준비물은 폰 앱 + 평소 쓰는 cloud AI + narratype 200자 뿐 — 자세한 건 **[STUDENT_PREP.md](STUDENT_PREP.md)** 참조 (15분 끝).
>
> **Installation is OPTIONAL.** The lecturer will demo this tool during the class — just watch and follow. Required workshop prep is only phone app + your usual cloud AI + 200-char narratype. See **[STUDENT_PREP.md](STUDENT_PREP.md)** (15 min).

---

## What it does / 무엇을 하는가

| Stage | English | 한국어 |
|---|---|---|
| 1 | Narratype Analysis — expand the scenario into Dator's 4 future archetypes | 시나리오를 4 archetype (성장·붕괴·지속·변혁)으로 확장 |
| 2 | AGENTS.md Authoring — draft a markdown protocol for AI agents in the speculative world | 시나리오 세계의 AI 협업 규칙 작성 (실제 industry 표준 markdown) |
| 3 | Audience Reaction — Nemotron-Personas-Korea react and classify by archetype | Nemotron 페르소나 30명이 작품에 반응 + archetype 분포 분석 |

Optional 4th agent (Futurist) generates 10 meta-questions based on Dator's Four Futures.
선택 4번째 에이전트 (미래학자)는 Dator 4 archetypes lens로 메타 질문 10개 생성.

---

## Key features / 핵심 기능

- **Bilingual UI** (한국어 / English) — toggle in sidebar
- **Persona Council** — upload Nemotron-Personas-Korea Excel, AI recommends 4 personas, they play the 4 roles in 1st-person
- **N-Round iteration** — 1-5 rounds, chairman output feeds back to mirror for refinement
- **Per-agent model selection** — different Ollama models for different roles
- **Class-wide Constellation tool** — aggregate visualization across multiple student outputs

---

## Quick start / 빠른 시작 (선택사항 · OPTIONAL)

> 학생들은 설치 안 해도 워크숍 참여 가능. 아래는 *"직접 돌려보고 싶은 분들"* 을 위한 가이드.
> Students don't need to install. Below is for those who want to run it themselves.

### Prerequisites / 전제

- macOS 11+ or Windows 10+
- 8GB RAM minimum (16GB recommended)
- 10GB free disk space
- Python 3.10+
- [Ollama](https://ollama.com) installed

### Install / 설치

```bash
# Pull the workshop standard models
ollama pull gemma4:e2b
ollama pull gemma4:e4b

# Get the code
git clone https://github.com/ers123/speculative-design-council.git
cd speculative-design-council

# Mac
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt

# Windows
python -m venv .venv
.venv\Scripts\activate
python -m pip install -r requirements.txt
```

### Run / 실행

```bash
streamlit run app.py
```

Browser opens automatically. Pick your language (한국어 / English) in the sidebar.

---

## Full installation guide / 상세 설치 가이드

See **[INSTALL.md](INSTALL.md)** — step-by-step bilingual guide covering both Mac and Windows, plus troubleshooting for the 9 most common issues.

상세한 설치 + 문제 해결 가이드는 **[INSTALL.md](INSTALL.md)** 참조.

## Why this design? / 왜 이렇게 디자인되었나?

처음 앱을 실행하면 *거울/지도/의장/미래학자, 4 archetype, Persona Council* 같은 용어들이 한꺼번에 보입니다. 헷갈리지 않게 **설계 의도**를 [WHY.md](WHY.md) 에 정리했습니다 (한·영 양국어).

When you first run the app, terms like *Mirror/Map/Chairman/Futurist, 4 archetypes, Persona Council* appear at once. See **[WHY.md](WHY.md)** for the design intent (bilingual). Recommended for first-time users.

## AGENTS.md 작성 가이드 / Authoring AGENTS.md

워크숍 Stage 2 산출물(`AGENTS.md`)을 학생이 직접·수동으로 어떻게 작성하는지, 도구가 자동 생성한 draft를 어떻게 다듬는지, 좋은 AGENTS.md의 기준은 무엇인지 — **[AGENTS_MD_GUIDE.md](AGENTS_MD_GUIDE.md)** 에 한·영 양국어로 정리 (HAPPY GATE 완성 예시 포함).

How students write the workshop's Stage 2 output (`AGENTS.md`) — both manually and by refining the tool's auto-draft. See **[AGENTS_MD_GUIDE.md](AGENTS_MD_GUIDE.md)** (bilingual, with full HAPPY GATE example).

추가 예시 — 4 도메인별 완성된 AGENTS.md (`examples/` 폴더):
- [HAPPY GATE](AGENTS_MD_GUIDE.md) (감정·정서) — in main guide
- [COCOO](examples/AGENTS_cocoo.md) (정체성·관계)
- [SPLIT](examples/AGENTS_split.md) (생태·환경)
- [SelectON](examples/AGENTS_selecton.md) (신체·웨어러블)

## 워크숍 운영 자료 / Workshop operation docs

워크숍 진행자(facilitator) + 학생 사전 준비용:
- **[STUDENT_PREP.md](STUDENT_PREP.md)** — 학생 사전 준비 안내 (한·영, 4가지 준비물 + 체크리스트)
- **[NARRATYPE_WORKSHEET.md](NARRATYPE_WORKSHEET.md)** — narratype 200자 작성 가이드 (한·영, 5 단계 + 2025 학생 예시 4개)
- **[ROLE_SPLIT.md](ROLE_SPLIT.md)** — 진행자 역할 분담 (HarmonyOn ↔ 박은선 교수님)
- **[BACKUP_PLAN.md](BACKUP_PLAN.md)** — 7가지 실패 시나리오 + 대응책

---

## Project structure / 프로젝트 구조

```
streamlit_spec_design_council/
├── app.py                  # Main Streamlit app
├── agents.py               # 12 system prompts (3 stages × 3 roles + advisor)
├── personas.py             # Nemotron persona loading + Council recommendation
├── exporters.py            # 5 export formats (docx, AGENTS.md, constellation, etc.)
├── resources.py            # File upload + grounding
├── sessions.py             # Session persistence
├── templates.py            # UI strings (i18n), stage descriptions, demo scenarios
├── class_constellation.py  # Class-wide visualization tool (standalone script)
├── smoke_test.py           # Structural test (Ollama not required)
├── e2e_test.py             # Mock E2E pipeline test
├── INSTALL.md              # Bilingual installation guide
├── DEMO_SCRIPT_SD.md       # 60-second hook demo script for workshop
├── CONVERSION.md           # Notes on fork from streamlit_research_team
└── requirements.txt
```

---

## Workshop context / 워크숍 맥락

Built for the Yonsei University 2026 Speculative Design class. The tool is used as:
1. A **demonstration** during the 1-hour workshop hook (instructor-led)
2. A **self-use tool** for students post-workshop (apply to their own narratypes)
3. A **class-wide aggregator** at semester end (Constellation visualization)

2026년 연세대 Speculative Design 수업용. 활용:
1. 1시간 워크숍 시연 (강사 진행)
2. 학생 자율 활용 (자기 narratype 발전)
3. 학기말 클래스 통합 (Constellation 시각화)

---

## Acknowledgments / 출처

- Base architecture forked from `streamlit_research_team` (HarmonyOn, 2026 Yonsei research workshop)
- Persona data: [nvidia/Nemotron-Personas-Korea](https://huggingface.co/datasets/nvidia/Nemotron-Personas-Korea) (CC-BY-4.0)
- Local LLM: [Google Gemma 4](https://ai.google.dev/gemma)
- Multi-agent inspiration: Karpathy's [llm-council](https://github.com/karpathy/llm-council)
- Pedagogical framework: Jim Dator's Four Futures, AGENTS.md community standard

## License

Apache 2.0 — see [LICENSE](LICENSE).

본 도구는 학생 작가적 결정을 대체하지 않습니다. AI 출력은 출발점일 뿐입니다.
This tool does not replace the student's authorial decisions. AI output is a starting point.
