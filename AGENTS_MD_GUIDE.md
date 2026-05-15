# AGENTS.md 작성 가이드 / Authoring Guide

> 본인의 narratype 세계 안에서 활동하는 AI 에이전트들의 협업 규칙(AGENTS.md)을 어떻게 쓰는가.
>
> How to write the AGENTS.md (collaboration protocol) for AI agents living inside your narratype world.

---

## 한국어 가이드

### 0. AGENTS.md가 무엇이고 왜 쓰는가?

**AGENTS.md** 는 2026년 현재 Anthropic·Google·OpenAI 등이 협업 AI 도구(Antigravity·Claude Code·Codex)에서 사용하는 **실제 산업 표준 markdown 파일**입니다. 한 시스템 안에서 작동하는 여러 AI 에이전트의 역할·권한·통신 규칙·검열 정책을 명시합니다.

본 워크숍에서는 학생이 자기 **narratype 세계 안의 AI 사회**를 디자인할 때 이 형식을 그대로 빌려옵니다. 즉, "2045년 너의 세계에 살고 있는 AI 에이전트들의 행동 강령"을 markdown으로 작성하는 것.

**왜 의미 있는가?**
- 학생 작품에 *"AI는 등장한다"* 가 아니라 *"AI는 이런 규칙으로 작동한다"* 가 명시됨
- 추상적 spec design을 **구체적 거버넌스 문서**로 떨어뜨림
- 진짜 markdown 표준이라 졸업 후 본인 프로젝트에도 쓸 수 있음

---

### 1. 두 가지 작성 경로

#### 경로 A — Streamlit Council Stage 2로 자동 draft (권장 시작)

1. 앱 실행 (`streamlit run app.py`)
2. 사이드바 단계 = **"AGENTS.md 작성"** 선택
3. 본문에 다음 입력:
   - **narratype 맥락** (Stage 1에서 했으면 자동 입력됨)
   - **핵심 갈등** 1줄 (예: "감정 검열 vs 표현 자유")
   - **AI가 다루는 영역** (신원 / 금융 / 감정 / 안전 / 노동 등 중 학생 선택)
4. **[Council 실행]** 클릭
5. 4명의 AI 에이전트(거울 → 지도 → 의장 → 미래학자[옵션])가 순차적으로:
   - 거울: 그 세계 AI 후보 5명 brainstorm + AGENTS.md 초안
   - 지도: 권한 구조·검열 정책 비평
   - 의장: 종합한 **최종 AGENTS.md** 출력
6. 우측 사이드바 또는 하단에서 **[AGENTS.md (.md) 다운로드]** 클릭
7. 다운로드한 .md 파일을 본인 markdown 에디터(Obsidian / Typora / VS Code 등)에서 열어 자유롭게 수정

→ AI는 *초안 작성자*, 본인은 *편집자·확정자*. AI 출력 그대로 제출 금지.

#### 경로 B — 수동 작성 (도구 없이 또는 보완 작성)

아래 템플릿을 본인 markdown 에디터에 복사 → 빈 칸 채우기.

```markdown
# AGENTS.md — [본인 narratype 세계명]
> 이 문서는 [세계명] 안에서 활동하는 AI 에이전트들의 행동 강령이다.
> 작성: [학생명] / 시기: 2045 / 버전: 1.0

## 1. 세계 환경
[2-3 문장으로 그 세계 묘사. 시기·장소·핵심 사건.]

## 2. 에이전트 명단
### 2.1 [에이전트 이름] (분류)
- 역할:
- 권한 수준: L1 / L2 / L3
- 통신 언어:
- 신뢰 등급:
- 시민 거부권: 가능 / 불가 / 제한적

### 2.2 [에이전트 이름] (분류)
(동일 형식, 최소 3명, 권장 5명)

## 3. 협업 프로토콜
### 3.1 우선순위 매트릭스
| 상황 | 우선 에이전트 | 기준 |
|---|---|---|
|   |   |   |

### 3.2 충돌 해결 (에이전트 간 의견 불일치 시)
1.
2.
3.

### 3.3 검열·차단 정책
- 차단 항목:
- 누가 결정하는가:
- 항소 가능 여부:

### 3.4 기록·감사
- 로그 형식:
- 보관 기간:
- 공개 범위:

## 4. 시민 인터페이스
[시민이 에이전트와 어떻게 만나는가. 강제 vs 선택. 거부권 어디까지.]

## 5. 책임 소재
[에이전트가 잘못된 결정을 내렸을 때 누가 책임지는가.]

## 6. 변경 이력
- 2045-XX-XX: 초기 작성 / [학생명]
```

권장: 경로 A로 초안 받은 후 경로 B 템플릿으로 본인이 한 번 다시 다듬기.

---

### 2. 완성 예시 — 박지우 "HAPPY GATE" (2025년 작품 기반)

본인 narratype을 어떻게 풀어내는지 감 잡으시라고 작성한 예시. **이대로 베끼지 말고** 본인 세계에 맞춰 새로 디자인.

```markdown
# AGENTS.md — HAPPY GATE 2045
> 이 문서는 2045년 서울 HAPPY GATE 사회 안에서 활동하는 AI 에이전트들의 행동 강령이다.
> 작성: 박지우 / 시기: 2045 / 버전: 1.0

## 1. 세계 환경
2045년 서울. 모든 공공시설(지하철·관공서·대형마트) 입구에 HAPPY GATE가 설치되어
안면 감정 분석 점수가 60점 미만이면 출입 거부. 시민은 매일 표정 점수 관리에 평균 47분 소비.

## 2. 에이전트 명단
### 2.1 EmoSentinel (정부)
- 역할: 게이트 통과 점수 실시간 산출
- 권한 수준: L3 (출입 결정권)
- 통신 언어: 시각 데이터 + 한국어 음성
- 신뢰 등급: 정부 인증
- 시민 거부권: 없음 (강제 통과)

### 2.2 SmileCoach (민간 기업 EmoEdge 운영)
- 역할: 표정 점수 향상 코칭, 거울 앞 5분 훈련 가이드
- 권한 수준: L1 (조언)
- 통신 언어: 한국어 + 미세표정 분석
- 신뢰 등급: 사적 계약
- 시민 거부권: 가능 (구독 해지)

### 2.3 EmoOmbud (시민단체)
- 역할: 게이트 거부 사례 분석, 헌법 소원 지원
- 권한 수준: L2 (조사 권한)
- 통신 언어: 한국어
- 신뢰 등급: 비영리
- 시민 거부권: 해당 없음 (시민 측)

### 2.4 ExpressionInspector (정부)
- 역할: 표정 단속관 — 게이트 점수 위조·필러 사용 적발
- 권한 수준: L2 (벌금 부과)
- 통신 언어: 한국어
- 신뢰 등급: 정부 인증
- 시민 거부권: 항소 가능 (행정심판)

### 2.5 NoSmileAdvocate (지하 시민 운동)
- 역할: 'No Smile Zone' 합법화 운동, 익명 표정 거부 캠페인
- 권한 수준: L0 (비공식)
- 통신 언어: 한국어 (암호화)
- 신뢰 등급: 비인증 (검열 대상)
- 시민 거부권: 자발 참여

## 3. 협업 프로토콜
### 3.1 우선순위 매트릭스
| 상황 | 우선 에이전트 | 기준 |
|---|---|---|
| 일상 출입 | EmoSentinel | 통과/거부 즉시 결정 |
| 점수 하락 시 | SmileCoach | 코칭 자동 시작 |
| 거부 누적 시 | EmoOmbud | 헌법소원 검토 |
| 점수 조작 의심 | ExpressionInspector | 단속 |

### 3.2 충돌 해결
1. EmoSentinel과 SmileCoach 충돌 시: 정부 우선
2. EmoOmbud와 ExpressionInspector 충돌 시: 헌법재판소 판단
3. 시민이 모든 에이전트를 거부할 때: NoSmileAdvocate 합류

### 3.3 검열·차단 정책
- 차단 항목: "표정 자유" 키워드, 게이트 우회 정보
- 누가 결정: 정부 위원회 (월 1회 심의)
- 항소 가능: 시민 단체 EmoOmbud 통해 7일 내

### 3.4 기록·감사
- 로그 형식: 게이트 통과 시각·점수·표정 데이터
- 보관 기간: 3년 (정부) / 1년 (민간)
- 공개 범위: 본인 + 영장 발부 시 사법기관

## 4. 시민 인터페이스
시민은 게이트를 거부할 권리가 **없음** (단, NoSmileAdvocate 운동 참여 가능).
SmileCoach 구독은 선택적. ExpressionInspector 단속에는 행정심판 가능.

## 5. 책임 소재
- 잘못된 점수 산출: EmoSentinel 운영 정부 (책임 회피 시 EmoOmbud 헌법 소원)
- 코칭 부작용 (표정 부담 우울증): SmileCoach 운영 기업
- 단속 오류: ExpressionInspector 소속 부처
- NoSmileAdvocate 활동가 체포: 인권 단체 개입

## 6. 변경 이력
- 2045-03-15: 초기 작성 / 박지우
```

---

### 3. 좋은 AGENTS.md 체크리스트

본인 작성본을 다음 5가지로 점검:

| # | 질문 | 통과 기준 |
|---|---|---|
| 1 | **권력 분포** | 한 에이전트에 권한이 집중되어 있지 않은가? 견제 구조가 보이는가? |
| 2 | **시민 거부권** | 어떤 결정을 시민이 거부할 수 있는지 명시되어 있는가? |
| 3 | **demographic 사각지대** | 어떤 시민층이 protocol에서 보호받지 못하는가? 그게 명시되어 있는가? |
| 4 | **항소·이의 절차** | 에이전트의 결정이 틀렸을 때 시민이 항소할 수 있는 경로가 있는가? |
| 5 | **책임 소재** | 잘못된 결정의 책임이 누구에게 있는지 추적 가능한가? |

5개 중 3개 이상 통과 → 첨부 가능한 수준. 5개 모두 통과 → 강한 작품.

---

### 4. 흔한 실수 (피해야 할 5가지)

| 실수 | 왜 문제인가 | 어떻게 고치나 |
|---|---|---|
| 에이전트가 다 정부 소속 | 권력 단일화. 견제 없음 | 민간·시민단체·지하 운동도 등장 |
| 권한 수준 모호 | "결정한다" 식의 추상 | L1/L2/L3 명시 (조언 / 조사 / 결정) |
| 시민 거부권 없음 | spec design의 본질 빠짐 | 최소 1명 에이전트에 시민 거부권 부여 |
| 책임 소재 공백 | "AI가 알아서 결정" 식 | 사람·기관 명시 |
| SF tropes 회귀 | "AI가 다 통제하는 디스토피아" | 한국 사회 특수성 적용 (구체적 부처·법령) |

---

### 5. 본인 narratype에 맞게 변형하는 팁

위 HAPPY GATE 예시는 **감정·정서** 도메인. 다른 도메인이면 에이전트 종류도 달라집니다:

- **신체·웨어러블** (예: SelectON 이어버드) → 청각 필터링 AI / 청각 단속관 / 청각 자유 운동
- **정체성·관계** (예: COCOO 자녀 CCTV) → 부모 알림 AI / 자녀 거부권 AI / 아동 보호 정부 부처
- **생태·환경** (예: SPLIT 기후 불평등) → 기후 점수 AI / 노동자 보험 AI / Bubble Tower 출입 통제
- **AI·자동화** → 메타 거버넌스 (AI가 AI를 감독)

도메인이 다르면 **에이전트 5명의 직군·소속·권한이 본인 세계에 자연스러워야** 합니다.

---

## English Guide

### 0. What is AGENTS.md and why use it?

**AGENTS.md** is a **real industry-standard markdown format** used in 2026 by Anthropic, Google, OpenAI, and others (Antigravity, Claude Code, Codex). It specifies roles, authority levels, communication rules, and censorship policies for multiple AI agents working within a single system.

For this workshop, you borrow that format to design the code of conduct for AI agents living in your narratype world in 2045.

**Why this matters:**
- Your spec design artifact moves from "AI exists" to "AI operates by these rules"
- Translates abstract speculation into a concrete governance document
- Uses a real markdown standard you can use in your own projects post-graduation

---

### 1. Two authoring paths

#### Path A — auto-draft via Streamlit Council Stage 2 (recommended start)

1. Run the app (`streamlit run app.py`)
2. In the sidebar, set Stage = **"AGENTS.md 작성"**
3. Provide:
   - **Narratype context** (auto-filled if you did Stage 1)
   - **Core conflict** in one line (e.g., "emotion surveillance vs expression freedom")
   - **AI domain** (identity / finance / emotion / safety / labor)
4. Click **[Run Council]**
5. The 4 AI agents (Mirror → Map → Chairman → Futurist[optional]) run sequentially:
   - Mirror: brainstorms 5 candidate agents + AGENTS.md draft
   - Map: critiques authority structure and censorship
   - Chairman: produces the synthesized **final AGENTS.md**
6. Download the **[AGENTS.md (.md)]** file from the export panel
7. Open in your markdown editor (Obsidian / Typora / VS Code) and revise freely

→ AI is the *drafter*; you are the *editor and final decider*. Don't submit AI output unchanged.

#### Path B — manual authoring (without tool or as refinement)

Copy the template below into your markdown editor; fill in the blanks.

```markdown
# AGENTS.md — [Your narratype world name]
> Code of conduct for AI agents acting in [world name].
> Author: [your name] / Time: 2045 / Version: 1.0

## 1. World Environment
[2-3 sentences describing the world. Time, place, key event.]

## 2. Agent Roster
### 2.1 [Agent Name] (Category)
- Role:
- Authority Level: L1 / L2 / L3
- Communication Language:
- Trust Rating:
- Citizen Veto: yes / no / limited

### 2.2 [Agent Name] (Category)
(Same format, min 3, recommended 5)

## 3. Collaboration Protocol
### 3.1 Priority Matrix
| Situation | Priority Agent | Criterion |
|---|---|---|
|   |   |   |

### 3.2 Conflict Resolution (when agents disagree)
1.
2.
3.

### 3.3 Censorship & Blocking Policy
- Blocked items:
- Decided by whom:
- Appeal possible:

### 3.4 Logging & Audit
- Log format:
- Retention period:
- Disclosure scope:

## 4. Citizen Interface
[How do citizens encounter the agents? Mandatory vs optional. Where is the veto?]

## 5. Accountability
[When an agent makes a wrong decision, who is responsible?]

## 6. Revision History
- 2045-XX-XX: initial draft / [your name]
```

Recommended: get a draft via Path A, then refine using Path B template.

---

### 2. Complete example (HAPPY GATE)

This example shows how to flesh out your own narratype. **Don't copy verbatim** — redesign for your own world.

```markdown
# AGENTS.md — HAPPY GATE 2045
> Code of conduct for AI agents acting within HAPPY GATE society in Seoul, 2045.
> Author: Park Ji-woo / Time: 2045 / Version: 1.0

## 1. World Environment
Seoul, 2045. HAPPY GATEs are installed at the entrance of every public facility (subways, government offices, large marts). Facial emotion analysis below a score of 60 results in entry denial. Citizens spend an average of 47 minutes per day managing their expression score.

## 2. Agent Roster
### 2.1 EmoSentinel (Government)
- Role: Real-time calculation of gate passage scores
- Authority level: L3 (entry decision authority)
- Communication language: Visual data + Korean voice
- Trust tier: Government-certified
- Citizen veto: None (forced passage)

### 2.2 SmileCoach (Private — operated by EmoEdge)
- Role: Expression score improvement coaching, 5-min mirror training guide
- Authority level: L1 (advice)
- Communication language: Korean + micro-expression analysis
- Trust tier: Private contract
- Citizen veto: Yes (cancel subscription)

### 2.3 EmoOmbud (Civic — Civil Liberties Coalition)
- Role: Analyzes gate-denial cases, supports constitutional petitions
- Authority level: L2 (investigation authority)
- Communication language: Korean
- Trust tier: Non-profit
- Citizen veto: Not applicable (advocates for citizen side)

### 2.4 ExpressionInspector (Government)
- Role: Expression enforcement officer — detects gate score forgery and filler use
- Authority level: L2 (fine imposition)
- Communication language: Korean
- Trust tier: Government-certified
- Citizen veto: Administrative appeal possible

### 2.5 NoSmileAdvocate (Underground — civic movement)
- Role: Movement to legalize 'No Smile Zones,' anonymous expression-refusal campaigns
- Authority level: L0 (informal)
- Communication language: Korean (encrypted)
- Trust tier: Uncertified (subject to censorship)
- Citizen veto: Voluntary participation

## 3. Collaboration Protocol
### 3.1 Priority matrix
| Situation | Lead agent | Criterion |
|---|---|---|
| Routine entry | EmoSentinel | Immediate pass/deny decision |
| Score drop | SmileCoach | Auto-coaching begins |
| Cumulative denials | EmoOmbud | Constitutional petition review |
| Suspected score manipulation | ExpressionInspector | Enforcement |

### 3.2 Conflict resolution
1. EmoSentinel vs SmileCoach: government takes priority
2. EmoOmbud vs ExpressionInspector: Constitutional Court judgment
3. When citizens reject all agents: NoSmileAdvocate joins in

### 3.3 Censorship & blocking policy
- Blocked items: "expression freedom" keyword, gate-bypass information
- Decision-maker: government committee (monthly review)
- Appeal: within 7 days via civic org EmoOmbud

### 3.4 Records & audit
- Log format: gate passage timestamp, score, facial data
- Retention: 3 years (government) / 1 year (private)
- Disclosure scope: self + law enforcement with warrant

## 4. Citizen Interface
Citizens have **no right** to refuse the gate (but may join NoSmileAdvocate movement).
SmileCoach subscription is optional. ExpressionInspector enforcement allows administrative appeal.

## 5. Accountability
- Wrong score calculation: EmoSentinel-operating government (EmoOmbud constitutional petition if government evades)
- Coaching side effects (expression-fatigue depression): SmileCoach-operating firm
- Enforcement errors: ExpressionInspector's ministry
- NoSmileAdvocate activist arrests: human rights organizations intervene

## 6. Revision History
- 2045-03-15: initial draft / Park Ji-woo
```

Key takeaways from the example:
- 5 agents from diverse origins (government, private, civic, watchdog, underground)
- Authority levels L0–L3 explicit
- Citizen veto specified per agent
- Appeal procedures named (constitutional court, ombudsman)
- Accountability traceable to specific actors

**Critique points to consider in your own work**:
- HAPPY GATE has no real citizen veto for the gate itself — that's the deliberate critique
- Where in *your* world does power concentrate? Make that visible

---

### 3. Quality checklist

Run your draft through these 5 questions:

| # | Question | Pass criterion |
|---|---|---|
| 1 | **Power distribution** | Is authority not concentrated in one agent? Are checks visible? |
| 2 | **Citizen veto** | Is it explicit which decisions citizens can refuse? |
| 3 | **Demographic blind spots** | Which citizens are not protected by the protocol? Is that explicit? |
| 4 | **Appeal procedures** | Can citizens appeal when an agent decides wrongly? |
| 5 | **Accountability** | Is responsibility traceable to specific actors/orgs? |

3+ pass → attachable quality. All 5 → strong work.

---

### 4. Common mistakes to avoid

| Mistake | Why it's a problem | How to fix |
|---|---|---|
| All agents government-affiliated | Power monopoly. No checks. | Add private/civic/underground actors |
| Vague authority | "Decides" without level | Specify L1/L2/L3 (advise / investigate / decide) |
| No citizen veto | Misses spec design point | At least 1 agent must have a citizen veto |
| Empty accountability | "AI decides somehow" | Name persons/institutions |
| SF tropes regression | "AI controls everything dystopia" | Apply Korean society specifics (real ministries, laws) |

---

### 5. Adapting to your narratype

The HAPPY GATE example is **emotion/affect** domain. Other domains imply different agent types:

- **Body/wearable** (e.g., SelectON earbuds) → Audio Filter AI / Audio Inspector / Audio Freedom Movement
- **Identity/relationship** (e.g., COCOO child CCTV) → Parent Alert AI / Child Veto AI / Child Protection Agency
- **Ecology/environment** (e.g., SPLIT climate inequality) → Climate Score AI / Worker Insurance AI / Bubble Tower Access Control
- **AI/automation** → Meta-governance (AI overseeing AI)

If the domain differs, **the 5 agents' professions, affiliations, and authority should fit your world naturally**.

---

## 참고 / Reference

- [agents.md](https://agents.md/) — community standard for AGENTS.md format
- [README.md](README.md) — overview and installation
- [WHY.md](WHY.md) — why this 4-agent design
- [INSTALL.md](INSTALL.md) — bilingual installation guide
- [DEMO_SCRIPT_SD.md](DEMO_SCRIPT_SD.md) — workshop demo script

Yonsei Speculative Design 2026 · AGENTS_MD_GUIDE.md
