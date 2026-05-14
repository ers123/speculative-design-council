# WHY — 이 도구는 왜 이렇게 디자인되었나 / Why is this tool designed this way?

> 처음 앱을 실행하면 거울/지도/의장/미래학자, 4 archetype, Persona Council 같은 용어들이 한꺼번에 보입니다. 헷갈릴 수 있어 설계 의도를 정리합니다.
>
> When you first run the app, you'll see terms like Mirror/Map/Chairman/Futurist, 4 archetypes, Persona Council all at once. This document explains the design intent.

---

## 한국어 가이드

### 1. 이 도구는 무엇을 하는가?

학생 본인의 narratype(미래 시나리오 + 거주 인물 + 세계관)을 **4명의 AI 에이전트가 함께 분석·확장·비평**하도록 도와줍니다. 결과물은 학생의 spec design 작품을 발전시키는 출발점이지, 정답이 아닙니다.

핵심 메시지 한 줄:
> **"AI는 도구가 아니라 디자인 재료다."**
> 학생은 사용자가 아니라 *재료를 다루는 작가·연출가*가 됩니다.

### 2. 왜 4명의 AI인가? (거울·지도·의장·미래학자)

**한 명의 AI에게 묻는 것**은 SF 영화의 "오라클" 같은 마법 상자입니다. 답은 매끈하지만 학생이 그 답을 *비판할 도구*가 없습니다.

**4명의 AI에게 동시에 묻는 것**은 *동료 심사·디자인 크리틱·시민 위원회*의 구조를 차용합니다. 한 명이 만들고, 한 명이 부수고, 한 명이 합치고, 한 명이 메타 질문을 던집니다. 학생은 *위원회의 의장*이 아니라 *위원회를 디자인한 사람*입니다.

#### 거울 (Mirror) — 폰의 로컬 AI 메타포
- **하는 일**: narratype을 4가지 미래 원형으로 *확장*. 가까이서 비추며 발산.
- **메타포 이유**: 폰의 Gemma 4 같은 로컬 AI는 작고·가깝고·사적이고·결함이 보임. 학생이 이미 손에 쥐고 있는 도구.

#### 지도 (Map) — 노트북·웹의 클라우드 AI 메타포
- **하는 일**: 거울의 확장을 *구조적·정치적*으로 비평. 사각지대·기술 결정론·SF tropes 회귀 지적.
- **메타포 이유**: ChatGPT·Claude 같은 클라우드 AI는 크고·멀고·공적이고·결함이 매끈하게 가려짐. 학생이 평소 쓰는 도구.

> **거울과 지도는 이 워크숍의 한 줄 메시지입니다.**
> 2026년 학생이 졸업 후 마주칠 세상은 이 둘이 *항상 공존*하는 세상. 어떤 일은 거울에 묻고 어떤 일은 지도에 묻는다. **이 둘 사이의 프로토콜을 누가 디자인하는가** — 이 워크숍이 학생에게 던지는 진짜 질문.

#### 의장 (Chairman) — 종합·결정
- **하는 일**: 거울과 지도의 *익명 peer review*를 받아 균형 잡힌 합성. 다음 발전 element 제시.
- **왜 필요한가**: 거울+지도만 있으면 두 의견이 갈리고 끝남. 학생이 다음 작업으로 가려면 종합·결정해주는 누군가 필요. *학술 동료 심사 모델*에서 차용.

#### 미래학자 (Futurist) — 선택 4번째 에이전트
- **하는 일**: 의장 종합 후 Dator의 4가지 미래(성장·붕괴·지속·변혁) lens로 *메타 질문 10개* 던짐.
- **왜 선택인가**: 학생 시간이 부족하면 끄고, 더 깊이 가고 싶으면 켜기. **사이드바 토글**로 제어.

### 3. 4 archetypes (성장·붕괴·지속·변혁)은 무엇?

미래학자 Jim Dator의 **Four Futures** 프레임워크입니다. 모든 미래 시나리오는 4가지 원형 중 하나(또는 혼합)로 분류 가능하다는 가설.

| Archetype | 한 줄 정의 | 예시 (HAPPY GATE 적용) |
|---|---|---|
| **성장 (Continued Growth)** | 현재 트렌드의 점진적 확장 | "더 정교한 게이트 — 미세표정까지 측정, AI 표정 코치 보급" |
| **붕괴 (Collapse)** | 시스템 실패·위기·후퇴 | "스마일 해커 등장, 진짜 표정 잃은 청년 세대" |
| **지속 (Discipline)** | 자제·규제·지속가능 모드 | "정부가 '감정노동 수당' 도입, 표정 단속관 직군 신설" |
| **변혁 (Transformation)** | 도약·post-human·새로운 차원 | "헌법재판소가 'No Smile Zone' 합법화" |

같은 narratype도 4 archetype 각각으로 펼치면 **4개의 다른 미래**가 나옵니다. 그게 Stage 1 (Narratype 분석)이 하는 일입니다.

### 4. Persona Council은 무엇? (사이드바 옵션)

위 4 역할(거울/지도/의장/미래학자)은 추상적 메타포입니다.

**Nemotron-Personas-Korea 페르소나 풀(Excel)을 업로드하면**, AI가 자동으로 4명의 실제 demographic 페르소나를 골라 *위 4 역할을 1인칭으로 연기*합니다.

그러면 "거울"이 *"전기태입니다, 광주 서구 70대 하역 노동자"* 가 되고, "지도"가 *"최은지입니다, 서초 회계 사무원"* 이 됩니다. 추상이 살아있는 인물·인격으로 옷이 바뀝니다.

**왜 의미 있는가**: 학생이 자기 narratype을 분석할 때 *본인과 가장 다른 demographic 4명*을 위원회로 부르면, 본인이 평소 보지 못하는 사각지대가 노출됩니다. 이게 spec design 정신 — AI가 도구가 아니라 *demographic 다양성을 가져오는 재료*.

### 5. 3단계의 의미

| 단계 | 무엇 | 기대 결과물 |
|---|---|---|
| **1. Narratype 분석** | 본인 시나리오를 4 archetype으로 확장 | 4개 다른 미래 + Constellation 좌표 |
| **2. AGENTS.md 작성** | 시나리오 세계의 AI들을 위한 협업 규칙 markdown 작성 | 학생 작품에 첨부 가능한 AGENTS.md 파일 |
| **3. 청중 반응 시뮬레이션** | 페르소나 30명이 작품에 반응하고 4 archetype으로 분류 | 청중 반응 보고서 + demographic 사각지대 분석 |

각 단계는 **같은 4-에이전트 하네스가 다른 시스템 프롬프트로 작동**합니다 (같은 코드, 다른 프롬프트 = "Harness Engineering").

### 6. 본인이 모든 걸 이해할 필요는 없습니다

이 도구는 **기본 설정 그대로 [Council 실행] 누르면 작동**합니다:
- 페르소나 미업로드 = 추상 Council (거울/지도/의장 메타포로 그대로 작동)
- 미래학자 모드 OFF = 3 에이전트만
- 라운드 1 = 단일 패스

위 설명은 "이 디자인이 왜 이렇게 됐는지" 궁금한 학생용입니다. 도구는 그냥 써도 작동합니다.

---

## English Guide

### 1. What does this tool do?

It helps you analyze, expand, and critique your own **narratype** (future scenario + inhabitants + worldview) with the help of **4 AI agents working together**. The output is a starting point for developing your spec design work — not a correct answer.

Core message:
> **"AI is not a tool, but a design material."**
> You're not just a user — you're an author/director working with that material.

### 2. Why 4 AI agents? (Mirror, Map, Chairman, Futurist)

**Asking one AI** is like consulting a sci-fi "oracle" — answers are smooth but you have no tool to *critique* them.

**Asking 4 AIs in dialogue** borrows from *academic peer review · design crit · civic council*. One generates, one criticizes, one synthesizes, one asks meta questions. You're the *designer of the council*, not its chairman.

#### Mirror — local-AI-on-your-phone metaphor
- **What it does**: Expands your narratype into 4 archetypes. Reflects closely, generatively.
- **Why this metaphor**: Local AI like Gemma 4 on your phone — small, close, private, flaws visible. A tool you already hold in your hand.

#### Map — cloud-AI-on-your-laptop metaphor
- **What it does**: Critiques Mirror's expansion structurally and politically. Points out blind spots, technological determinism, SF-tropes regression.
- **Why this metaphor**: Cloud AI like ChatGPT/Claude — large, distant, public, flaws smoothly hidden. The tool you use daily.

> **Mirror and Map are the workshop's one-line message.**
> By 2026, after graduation, you'll live in a world where these two coexist *always*. Some questions you ask Mirror; others you ask Map. **Who designs the protocol between them?** — that's the real question this workshop poses to you.

#### Chairman — synthesis & decision
- **What it does**: Receives anonymous peer review from Mirror and Map, produces a balanced synthesis, proposes next development element.
- **Why needed**: Without Chairman, Mirror+Map just leaves two disagreeing voices. You need someone to synthesize for you to move on to next work. Borrowed from *academic peer review model*.

#### Futurist — optional 4th agent
- **What it does**: After Chairman's synthesis, asks 10 meta-questions through Dator's Four Futures lens.
- **Why optional**: Turn off if short on time; turn on for depth. Controlled by **sidebar toggle**.

### 3. What are the 4 archetypes (Growth, Collapse, Discipline, Transformation)?

This is **Jim Dator's Four Futures** framework. Hypothesis: every future scenario can be classified into one (or a mix) of 4 archetypes.

| Archetype | One-line definition | Example (applied to HAPPY GATE) |
|---|---|---|
| **Continued Growth** | Gradual extension of current trends | "More refined gates — measuring micro-expressions, AI expression coaches" |
| **Collapse** | System failure, crisis, retreat | "Smile hackers emerge; a generation that has forgotten real expression" |
| **Discipline** | Restraint, regulation, sustainability mode | "Government introduces 'emotion labor wage', expression inspector as new job category" |
| **Transformation** | Leap, post-human, new dimension | "Constitutional Court legalizes 'No Smile Zone'" |

The same narratype, expanded through 4 archetypes, gives you **4 different futures**. That's what Stage 1 (Narratype Analysis) does.

### 4. What is Persona Council? (sidebar option)

The 4 roles above (Mirror/Map/Chairman/Futurist) are abstract metaphors.

**If you upload a Nemotron-Personas-Korea persona pool (Excel)**, AI automatically picks 4 real demographic personas to *play those 4 roles in 1st person*.

Then "Mirror" becomes *"Hi, I'm Jeon Gi-tae, a 70s laborer from Gwangju"*, and "Map" becomes *"Hi, I'm Choi Eun-ji, an accountant in Seocho, Seoul"*. The abstract becomes living individuals.

**Why this matters**: When analyzing your narratype, summoning *4 personas most different from yourself* as the council exposes blind spots you usually don't see. This is the spec design spirit — AI not as a tool but as a *material that brings demographic diversity*.

### 5. What each of the 3 stages does

| Stage | What | Expected output |
|---|---|---|
| **1. Narratype Analysis** | Expand your scenario into 4 archetypes | 4 different futures + Constellation coordinates |
| **2. AGENTS.md authoring** | Write a markdown protocol for AI agents in your speculative world | AGENTS.md file you can attach to your spec design artifact |
| **3. Audience Reaction** | 30 personas react to your work, classified by 4 archetypes | Audience report + demographic blind-spot analysis |

Each stage runs **the same 4-agent harness with different system prompts** (same code, different prompts = "Harness Engineering").

### 6. You don't need to understand all of this

The tool **works fine on default settings** — just click [Run Council]:
- No persona uploaded = abstract Council (Mirror/Map/Chairman metaphors as-is)
- Futurist mode OFF = 3 agents only
- 1 round = single pass

The explanation above is for students curious about *why this design exists*. The tool runs regardless.

---

## 더 자세한 출처 / More on the design source

이 4-에이전트 패턴은 본인의 이전 작업 [`streamlit_research_team`](../demo/streamlit_research_team) (대학원 연구 설계 도우미)에서 가져왔습니다. 같은 하네스 × 다른 프롬프트 = 다른 도메인.

This 4-agent pattern is forked from the upstream [`streamlit_research_team`](../demo/streamlit_research_team) (graduate research design assistant). Same harness × different prompts = different domain.

Persona Council layer and Dator 4 archetypes integration are 2026 SD workshop specific additions.

---

## 관련 자료 / Related docs

- [README.md](README.md) — overview and installation
- [INSTALL.md](INSTALL.md) — bilingual installation guide
- [DEMO_SCRIPT_SD.md](DEMO_SCRIPT_SD.md) — 60s hook demo script for workshop
- [CONVERSION.md](CONVERSION.md) — fork conversion log from `streamlit_research_team`

Yonsei Speculative Design 2026 · WHY.md last updated 2026.05.11
