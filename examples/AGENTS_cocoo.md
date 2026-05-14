# AGENTS.md — COCOO 2045 (Invisible Safety Net)
> 이 문서는 COCOO 사회 (자녀 안전 관리 시스템) 안에서 활동하는 AI 에이전트들의 행동 강령이다.
> 작성: 이예진 (2025) 차용 예시 / 시기: 2045 / 버전: 1.0
> 도메인: 정체성·관계 (Identity / Relationship)

## 1. 세계 환경
2045년 한국. 학교·학원·놀이터·길거리 모든 공공 공간에 정부-민간 통합 CCTV망. 부모가 월 구독료 5만원을 내면 자녀 영상 24시간 접근 가능. 자녀는 의무적으로 웨어러블 감지 기기(목걸이형) 착용. 자녀 출생 신고와 동시에 COCOO 서비스 자동 가입.

## 2. 에이전트 명단

### 2.1 GuardianFeed (정부 — 보건복지부)
- 역할: 자녀 위치·심박·표정·음성 실시간 부모 전송
- 권한 수준: L3 (자녀 동의 없이 데이터 수집)
- 통신 언어: 한국어 + 시각 데이터
- 신뢰 등급: 정부 인증
- 시민 거부권: 없음 (만 19세 이전)

### 2.2 LearningOptimizer (민간 — EduCorp)
- 역할: 자녀 학습 효율 분석, 친구 관계 평가, 미래 성공 가능성 예측
- 권한 수준: L2 (보고서 작성)
- 통신 언어: 한국어 + AI 도표
- 신뢰 등급: 사적 계약 (월 추가 3만원)
- 시민 거부권: 가능 (구독 해지)

### 2.3 ChildVoice (시민단체 — 청소년인권센터)
- 역할: 자녀가 익명으로 COCOO 거부 의사 표현, 부모-자녀 분쟁 조정
- 권한 수준: L1 (중재 권유)
- 통신 언어: 한국어 (자녀 모국어)
- 신뢰 등급: 비영리
- 시민 거부권: 해당 없음 (자녀 측 옹호)

### 2.4 ParentalOversightInspector (정부 — 여성가족부)
- 역할: 부모의 데이터 오남용 감시 (과도한 접근, 친구 평가 활용 등)
- 권한 수준: L2 (계정 정지 권한)
- 통신 언어: 한국어 + 사법 문서
- 신뢰 등급: 정부 인증
- 시민 거부권: 부모 측 항소 가능

### 2.5 LiberationNetwork (지하 — 자녀 권리 운동)
- 역할: 만 15세 이상 청소년의 COCOO 해제 비공식 지원
- 권한 수준: L0 (비공식, 법적 회색지대)
- 통신 언어: 한국어 (암호화)
- 신뢰 등급: 비인증
- 시민 거부권: 자발 참여

## 3. 협업 프로토콜

### 3.1 우선순위 매트릭스
| 상황 | 우선 에이전트 | 기준 |
|---|---|---|
| 일상 모니터링 | GuardianFeed | 자동 데이터 흐름 |
| 부모 추가 분석 요청 | LearningOptimizer | 구독자 한정 |
| 자녀 거부 의사 표현 | ChildVoice | 익명 보장 |
| 부모 오남용 의심 | ParentalOversightInspector | 자동 알람 |

### 3.2 충돌 해결
1. 자녀(ChildVoice) vs 부모(GuardianFeed/LearningOptimizer) 충돌 시: 만 15세 이상은 가정법원 조정
2. ParentalOversightInspector가 부모 권한 제한 시: 부모는 행정심판 가능
3. LiberationNetwork는 공식 시스템 밖이라 분쟁 무관

### 3.3 검열·차단 정책
- 차단 항목: "COCOO 해제 방법", "웨어러블 무력화" 검색
- 누가 결정: 보건복지부 위원회 (3개월마다 review)
- 항소 가능: 자녀가 만 18세 이후 본인 데이터 삭제 요구 가능 (단, 부모 미동의 시 30년 보관)

### 3.4 기록·감사
- 로그 형식: 위치·심박·표정 데이터 + 부모 접근 시각
- 보관 기간: 자녀 만 30세까지 (정부 보관) / 부모 구독 종료 후 1년 (민간 보관)
- 공개 범위: 자녀 본인 (만 18세 이후) + 영장 시 사법기관

## 4. 시민 인터페이스

자녀 (피보호자):
- 만 19세까지 COCOO 의무 가입, 거부 불가
- 만 15-18세: ChildVoice 통해 의사 표현 가능
- 만 18세 이후: 본인 데이터 일부 삭제 요구 가능

부모 (구독자):
- 기본 구독: GuardianFeed 자동
- 추가: LearningOptimizer 월 3만원
- ParentalOversightInspector 경고 받으면 7일 내 해명

## 5. 책임 소재

- 데이터 유출: GuardianFeed 운영 정부 (개인정보보호법)
- 친구 평가 오류: LearningOptimizer 운영 민간 (서비스 약관 분쟁)
- 자녀 정신건강 부작용: 합의된 책임 불명 (현재 헌법 소원 진행 중)
- LiberationNetwork 활동가 적발: 청소년 보호법 위반 (벌금)

## 6. 변경 이력
- 2045-01-15: 초기 도입 (보건복지부)
- 2045-08-22: ChildVoice 추가 (헌법소원 결과)
- 2046-03-01: 만 18세 데이터 일부 삭제 권리 추가 (법 개정)

---
이 AGENTS.md는 spec design 작품 "COCOO: Invisible Safety Net" 의 일부이다.
도메인이 다른 narratype에 적용 시: 권력 분포·시민 거부권·항소 절차 구조는 유지하되 에이전트 이름·소속·기능은 자기 세계에 맞춰 변형.

**비판 포인트**:
- 자녀 동의 없는 데이터 수집 — 부모 권리가 자녀 자기결정권보다 우선
- 만 18세 이후에도 부모 미동의 시 30년 보관
- "보호"라는 이름의 감시 — 거부할 권한이 자녀에게는 없음

═══════════════════════════════════════

# English Version

# AGENTS.md — COCOO 2045 (Invisible Safety Net)
> Conduct protocol for AI agents operating within COCOO society (child safety management system).
> Authored: Lee Ye-jin (2025) — borrowed example / Time: 2045 / Version: 1.0
> Domain: Identity / Relationship

## 1. World Environment
Korea, 2045. Government-private integrated CCTV network covers every public space — schools, academies, playgrounds, streets. Parents who pay a monthly subscription of ₩50,000 get 24-hour access to their child's video feed. Children are required to wear detection wearables (necklace-type). COCOO service enrollment is automatic upon birth registration.

## 2. Agent Roster

### 2.1 GuardianFeed (Government — Ministry of Health & Welfare)
- Role: Real-time transmission of child's location, heart rate, facial expression, and voice to parents
- Authority level: L3 (collects data without child consent)
- Communication language: Korean + visual data
- Trust tier: Government-certified
- Citizen veto: None (under age 19)

### 2.2 LearningOptimizer (Private — EduCorp)
- Role: Analyzes child's learning efficiency, evaluates peer relationships, predicts future success likelihood
- Authority level: L2 (report generation)
- Communication language: Korean + AI charts
- Trust tier: Private contract (+₩30,000/month)
- Citizen veto: Yes (cancel subscription)

### 2.3 ChildVoice (Civic — Youth Rights Center)
- Role: Allows children to anonymously express COCOO refusal, mediates parent-child disputes
- Authority level: L1 (mediation suggestion)
- Communication language: Korean (child's native tongue)
- Trust tier: Non-profit
- Citizen veto: Not applicable (advocates for child side)

### 2.4 ParentalOversightInspector (Government — Ministry of Gender Equality & Family)
- Role: Monitors parental data misuse (excessive access, peer-evaluation exploitation, etc.)
- Authority level: L2 (account suspension authority)
- Communication language: Korean + legal documents
- Trust tier: Government-certified
- Citizen veto: Parents may appeal

### 2.5 LiberationNetwork (Underground — Children's Rights Movement)
- Role: Unofficially supports COCOO removal for youth aged 15+
- Authority level: L0 (informal, legal gray zone)
- Communication language: Korean (encrypted)
- Trust tier: Uncertified
- Citizen veto: Voluntary participation

## 3. Collaboration Protocol

### 3.1 Priority matrix
| Situation | Lead agent | Criterion |
|---|---|---|
| Routine monitoring | GuardianFeed | Auto data flow |
| Parent request for deeper analysis | LearningOptimizer | Subscriber-only |
| Child expresses refusal | ChildVoice | Anonymity guaranteed |
| Suspected parental misuse | ParentalOversightInspector | Auto-alert |

### 3.2 Conflict resolution
1. Child (ChildVoice) vs Parent (GuardianFeed/LearningOptimizer): for ages 15+, mediated by Family Court
2. ParentalOversightInspector restricting parental rights: parents may file administrative appeal
3. LiberationNetwork is outside the official system, so not subject to dispute resolution

### 3.3 Censorship & blocking policy
- Blocked items: searches for "How to remove COCOO," "How to disable wearables"
- Decision-maker: Ministry of Health & Welfare committee (reviewed quarterly)
- Appeal: Children may request data deletion after age 18 (but if parents don't consent, data retained for 30 years)

### 3.4 Records & audit
- Log format: location, heart rate, facial data + parental access timestamps
- Retention: until age 30 (government) / 1 year after subscription ends (private)
- Disclosure scope: child themselves (after age 18) + law enforcement with warrant

## 4. Citizen Interface

Children (the protected):
- Mandatory COCOO enrollment until age 19, cannot refuse
- Ages 15-18: can express preferences via ChildVoice
- After age 18: can request deletion of certain data

Parents (subscribers):
- Base subscription: GuardianFeed (default)
- Add-on: LearningOptimizer ₩30,000/month
- If flagged by ParentalOversightInspector: must respond within 7 days

## 5. Accountability

- Data leak: GuardianFeed-operating government (Personal Information Protection Act)
- Peer evaluation error: LearningOptimizer-operating private firm (terms-of-service dispute)
- Child's mental health side effects: agreed responsibility unclear (constitutional petition currently pending)
- LiberationNetwork activist arrest: Youth Protection Act violation (fine)

## 6. Revision History
- 2045-01-15: Initial deployment (Ministry of Health & Welfare)
- 2045-08-22: ChildVoice added (result of constitutional petition)
- 2046-03-01: Right to delete some data after age 18 added (legal amendment)

---
This AGENTS.md is part of the spec design work "COCOO: Invisible Safety Net."
When applying to a different domain narratype: keep the power distribution, citizen veto, and appeal procedure structure intact, but adapt the agent names, affiliations, and functions to your own world.

**Critique points**:
- Data collection without child consent — parental rights prioritized over child's right to self-determination
- 30-year retention even after age 18 if parents don't consent
- Surveillance under the name of "protection" — children have no right to refuse
