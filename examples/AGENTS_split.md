# AGENTS.md — SPLIT 2045 (Climate Stratification)
> 이 문서는 SPLIT 사회 (기후 위기의 계급 분리) 안에서 활동하는 AI 에이전트들의 행동 강령이다.
> 작성: 심영석 (2025) 차용 예시 / 시기: 2045 / 버전: 1.0
> 도메인: 생태·환경 (Ecology / Environment)

## 1. 세계 환경
2045년 한국. 폭염·홍수·산불·미세먼지가 일상이 된 사회. 상위 10%는 'Bubble Towers'(실내 정수·필터·항온·항습) 거주, 하위 30%는 '기후 노동자'(폭염 속 배달, 미세먼지 속 청소). 평균 수명 격차 12년. AI는 이 격차를 *"개인의 직업 선택"* 으로 설명하고 자동화한다.

## 2. 에이전트 명단

### 2.1 ClimateScoreAI (정부 — 환경부)
- 역할: 시민별 기후 노출 위험도 점수 산출. Bubble Tower 우선 입주권 결정.
- 권한 수준: L3 (생존 인프라 분배 권한)
- 통신 언어: 한국어 + 점수 시각화
- 신뢰 등급: 정부 인증
- 시민 거부권: 없음 (자동 적용)

### 2.2 WorkerInsuranceBot (민간 — 기후 노동자 보험)
- 역할: 기후 노동자 출근 가능 여부 판정 (폭염 지수 기반), 병가 처리
- 권한 수준: L2 (휴무 명령)
- 통신 언어: 한국어 + 출근 카드
- 신뢰 등급: 사적 계약 (월 5만원, 사실상 강제)
- 시민 거부권: 비가입 시 무보험 (사고 자기책임)

### 2.3 BubbleAccessGuard (민간 — Bubble Tower 운영사)
- 역할: Bubble Tower 출입 통제, 입주자·방문자 검증
- 권한 수준: L3 (출입 거부 권한)
- 통신 언어: 영어 (입주자 글로벌 기준)
- 신뢰 등급: 사적 계약
- 시민 거부권: 외부인은 항소 절차 없음

### 2.4 ClimateOmbud (시민단체 — 기후정의연대)
- 역할: 노동자 사망 사례 분석, ClimateScoreAI 알고리즘 감사, 헌법소원 지원
- 권한 수준: L1 (조사·공시)
- 통신 언어: 한국어
- 신뢰 등급: 비영리 (해외 펀딩 의존)
- 시민 거부권: 해당 없음 (노동자 측 옹호)

### 2.5 OutsideMovement (비공식 — 'Outside Air' 시민운동)
- 역할: Bubble Tower 거부, 외부 공기에서 살자는 운동. 농촌 자급 공동체.
- 권한 수준: L0 (비공식)
- 통신 언어: 한국어
- 신뢰 등급: 비인증 (정부가 "보건 위험" 분류)
- 시민 거부권: 자발 참여

## 3. 협업 프로토콜

### 3.1 우선순위 매트릭스
| 상황 | 우선 에이전트 | 기준 |
|---|---|---|
| 폭염 경보 | WorkerInsuranceBot | 자동 휴무 또는 출근 명령 |
| Bubble 입주 신청 | ClimateScoreAI → BubbleAccessGuard | 점수 + 자산 검증 |
| 노동자 사망 발생 | ClimateOmbud | 자동 조사 시작 |
| 사망률 알고리즘 의심 | ClimateOmbud → 헌법재판소 | 공익 소송 |

### 3.2 충돌 해결
1. ClimateScoreAI vs ClimateOmbud 충돌 시: 환경부 위원회 (단, 위원의 30%가 노동계)
2. BubbleAccessGuard vs ClimateScoreAI 충돌 시 (정부 vs 민간): 정부 우선
3. OutsideMovement 활동가는 시스템 밖이라 분쟁 무관

### 3.3 검열·차단 정책
- 차단 항목: "ClimateScoreAI 알고리즘 공개", "Bubble Tower 결함 정보"
- 누가 결정: 환경부 위원회 + 기업 협의체
- 항소 가능: ClimateOmbud 헌법소원 (평균 3년 소요)

### 3.4 기록·감사
- 로그 형식: 시민별 기후 노출 시간·점수·입주 결정
- 보관 기간: 50년 (정부) / 5년 (민간)
- 공개 범위: 본인 (단, 알고리즘 공개 X) + 영장 시 사법기관

## 4. 시민 인터페이스

상위 10% (Bubble 거주자):
- ClimateScoreAI 점수 자동 우대
- BubbleAccessGuard 통과 자동
- 외부 공기 노출 거의 없음

중산층 (30%):
- 마스크·청정기 자가 부담
- ClimateScoreAI 점수 중간
- Bubble Tower 입주 대기 평균 7년

기후 노동자 (30%):
- WorkerInsuranceBot 강제 가입
- 폭염 출근 거부 시 휴업 (생계 위기)
- ClimateOmbud 통해서만 권리 보호

## 5. 책임 소재

- 노동자 폭염 사망: WorkerInsuranceBot 운영 민간 (책임 회피 시 ClimateOmbud)
- Bubble Tower 입주자 시설 사고: BubbleAccessGuard 운영 민간
- ClimateScoreAI 알고리즘 차별: 환경부 (헌법소원 인용 사례 0건)
- OutsideMovement 활동가 사망 (외부 노출): 본인 책임 (정부 입장)

## 6. 변경 이력
- 2044-08-15: 폭염 사망 1만 명 초과 — 시민운동 시작
- 2045-01-01: 본 AGENTS.md 시행 (환경부)
- 2045-06-22: ClimateOmbud 강제 포함 (헌법소원 결과)

---
이 AGENTS.md는 spec design 작품 "SPLIT: Climate Stratification" 의 일부이다.

**비판 포인트**:
- 알고리즘 공개 차단 → 차별 추적 불가
- "자발 참여" 표현이 노동자에게는 비자발적 강제
- OutsideMovement 사망을 "자기책임"으로 묶는 정부 논리

═══════════════════════════════════════

# English Version

# AGENTS.md — SPLIT 2045 (Climate Stratification)
> Conduct protocol for AI agents operating within SPLIT society (class division under climate crisis).
> Authored: Shim Young-seok (2025) — borrowed example / Time: 2045 / Version: 1.0
> Domain: Ecology / Environment

## 1. World Environment
Korea, 2045. Heatwaves, floods, wildfires, and fine dust have become routine. The top 10% live in 'Bubble Towers' (indoor air filtration, climate control, thermostat). The bottom 30% are 'climate workers' (delivery in scorching heat, cleaning in fine dust). Average life expectancy gap: 12 years. AI explains this gap as *"individual career choice"* and automates it.

## 2. Agent Roster

### 2.1 ClimateScoreAI (Government — Ministry of Environment)
- Role: Calculates each citizen's climate exposure risk score. Determines Bubble Tower entry priority.
- Authority level: L3 (authority over survival infrastructure distribution)
- Communication language: Korean + score visualizations
- Trust tier: Government-certified
- Citizen veto: None (auto-applied)

### 2.2 WorkerInsuranceBot (Private — Climate Worker Insurance)
- Role: Determines climate workers' eligibility to work (based on heat index), processes sick leave
- Authority level: L2 (authority to mandate rest days)
- Communication language: Korean + work permit cards
- Trust tier: Private contract (₩50,000/month, effectively mandatory)
- Citizen veto: Non-enrollment leaves worker uninsured (accidents are self-liability)

### 2.3 BubbleAccessGuard (Private — Bubble Tower Operator)
- Role: Controls Bubble Tower entry, verifies residents and visitors
- Authority level: L3 (entry refusal authority)
- Communication language: English (residents are global elites)
- Trust tier: Private contract
- Citizen veto: Outsiders have no appeal process

### 2.4 ClimateOmbud (Civic — Climate Justice Alliance)
- Role: Analyzes worker deaths, audits ClimateScoreAI algorithm, supports constitutional petitions
- Authority level: L1 (investigation, public disclosure)
- Communication language: Korean
- Trust tier: Non-profit (dependent on overseas funding)
- Citizen veto: Not applicable (advocates for worker side)

### 2.5 OutsideMovement (Informal — 'Outside Air' civic movement)
- Role: Rejects Bubble Towers, advocates living in outside air. Rural self-sufficient communes.
- Authority level: L0 (informal)
- Communication language: Korean
- Trust tier: Uncertified (government classifies as "health hazard")
- Citizen veto: Voluntary participation

## 3. Collaboration Protocol

### 3.1 Priority matrix
| Situation | Lead agent | Criterion |
|---|---|---|
| Heat alert | WorkerInsuranceBot | Auto rest-day or work-day mandate |
| Bubble entry application | ClimateScoreAI → BubbleAccessGuard | Score + asset verification |
| Worker death occurs | ClimateOmbud | Auto investigation |
| Mortality algorithm suspected | ClimateOmbud → Constitutional Court | Public interest lawsuit |

### 3.2 Conflict resolution
1. ClimateScoreAI vs ClimateOmbud: Ministry of Environment committee (but 30% of members are from labor)
2. BubbleAccessGuard vs ClimateScoreAI (private vs government): government takes priority
3. OutsideMovement activists are outside the system, not subject to dispute resolution

### 3.3 Censorship & blocking policy
- Blocked items: "ClimateScoreAI algorithm disclosure," "Bubble Tower defect information"
- Decision-maker: Ministry of Environment committee + corporate consortium
- Appeal: ClimateOmbud constitutional petition (average 3 years to resolve)

### 3.4 Records & audit
- Log format: per-citizen climate exposure time, score, entry decisions
- Retention: 50 years (government) / 5 years (private)
- Disclosure scope: self (but algorithm not disclosed) + law enforcement with warrant

## 4. Citizen Interface

Top 10% (Bubble residents):
- ClimateScoreAI scores auto-favorable
- BubbleAccessGuard passage automatic
- Almost no outside air exposure

Middle class (30%):
- Self-pays for masks and air purifiers
- ClimateScoreAI score: middle
- Bubble Tower entry waitlist: average 7 years

Climate workers (30%):
- Mandatory WorkerInsuranceBot enrollment
- Refusing work during heatwave means business closure (livelihood crisis)
- Rights protected only via ClimateOmbud

## 5. Accountability

- Worker heatstroke death: WorkerInsuranceBot-operating private firm (ClimateOmbud steps in if firm evades)
- Bubble Tower resident facility accidents: BubbleAccessGuard-operating private firm
- ClimateScoreAI algorithm discrimination: Ministry of Environment (constitutional petitions sustained: 0)
- OutsideMovement activist death (outside exposure): self-liability (government position)

## 6. Revision History
- 2044-08-15: Heat deaths exceed 10,000 — civic movement begins
- 2045-01-01: This AGENTS.md takes effect (Ministry of Environment)
- 2045-06-22: ClimateOmbud forced into inclusion (result of constitutional petition)

---
This AGENTS.md is part of the spec design work "SPLIT: Climate Stratification."

**Critique points**:
- Algorithm disclosure blocked → discrimination cannot be tracked
- The phrase "voluntary participation" is involuntary coercion for workers
- Government logic that frames OutsideMovement deaths as "self-liability"
