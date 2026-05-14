# AGENTS.md — SelectON 2045 (Auditory Stratification)
> 이 문서는 SelectON 사회 (자발적 청각 분리) 안에서 활동하는 AI 에이전트들의 행동 강령이다.
> 작성: 박혜준 (2025) 차용 예시 / 시기: 2045 / 버전: 1.0
> 도메인: 신체·웨어러블 (Body / Wearable)

## 1. 세계 환경
2045년 한국. 무선 이어버드 'SelectON' 보급률 95%. 사용자는 24시간 착용하며 듣고 싶은 소리만 선택. 가족·동료·이웃 목소리도 *"구독"* 해야 들림. 우는 아기, 거리 시위, 노숙자 외침은 자동 필터링. *"소음 공해 0%"* 자랑하지만 실은 *"타인 0%"* 사회.

## 2. 에이전트 명단

### 2.1 SoundFilterCore (민간 — SelectON Inc.)
- 역할: 사용자별 청각 필터링 (소음 분류, 자동 차단, 음량 조절)
- 권한 수준: L3 (실시간 차단 결정)
- 통신 언어: 자연어 음성 명령 (한·영)
- 신뢰 등급: 사적 계약 (월 9.9만원)
- 시민 거부권: 가능 (이어버드 미착용)

### 2.2 EmergencyOverride (정부 — 안전처)
- 역할: 응급 사이렌·재난 방송 강제 송출 (필터링 우회)
- 권한 수준: L3 (필수 알림)
- 통신 언어: 한국어 + 진동
- 신뢰 등급: 정부 인증
- 시민 거부권: 없음 (생존 인프라)

### 2.3 SocialEmpathyMonitor (민간 — Big Tech 광고 모델)
- 역할: 사용자가 차단한 소리 패턴 분석 → 맞춤 광고
- 권한 수준: L2 (데이터 수집·판매)
- 통신 언어: 한국어 + 광고 음성
- 신뢰 등급: 사적 계약 (광고 기반 = 무료 구독)
- 시민 거부권: 유료 구독으로 광고 OFF

### 2.4 NoiseRightsAdvocate (시민단체 — 청각공감연대)
- 역할: 노숙자·시위자·우는 아기 등 "필터링된 사람들" 권리 옹호
- 권한 수준: L1 (조사·공시)
- 통신 언어: 한국어
- 신뢰 등급: 비영리
- 시민 거부권: 해당 없음 (필터링되는 측 옹호)

### 2.5 ResonanceCircle (지하 — 'Listen Together' 비공식 모임)
- society
- 역할: 이어버드 빼고 공동 청취하는 카페·공원 운영
- 권한 수준: L0 (비공식)
- 통신 언어: 한국어 (대면)
- 신뢰 등급: 비인증
- 시민 거부권: 자발 참여

## 3. 협업 프로토콜

### 3.1 우선순위 매트릭스
| 상황 | 우선 에이전트 | 기준 |
|---|---|---|
| 일상 필터링 | SoundFilterCore | 자동 분류 |
| 재난·응급 | EmergencyOverride | 강제 송출 (필터 무효) |
| 광고 송출 | SocialEmpathyMonitor | 무료 사용자만 |
| 필터링 차별 의심 | NoiseRightsAdvocate | 조사·고발 |

### 3.2 충돌 해결
1. SoundFilterCore vs EmergencyOverride 충돌 시: 정부 우선
2. SocialEmpathyMonitor 데이터 오남용 시: 개인정보보호위원회 조사
3. ResonanceCircle은 시스템 밖이라 분쟁 무관 (단, 공원 점유 시 경범죄)

### 3.3 검열·차단 정책
- 차단 항목: "필터링 해킹", "응급 알림 비활성화"
- 누가 결정: SelectON Inc. 정책팀 (정부 가이드라인 따름)
- 항소 가능: 사용자가 본인 필터 로그 30일 내 review 가능

### 3.4 기록·감사
- 로그 형식: 차단된 소리 유형·시각·위치 (개인 식별)
- 보관 기간: 7년 (민간 광고 모델)
- 공개 범위: 본인 (단, 광고 추론 알고리즘 비공개) + 영장 시 사법기관

## 4. 시민 인터페이스

이어버드 착용자 (95%):
- 자동 필터링 — 차단 항목 본인이 직접 추가 가능
- 광고 OFF 원하면 유료 구독
- 응급 알림은 절대 차단 불가

필터링되는 측 (5% + 무수한 익명):
- 노숙자·시위자·우는 아기·거리 음악가
- NoiseRightsAdvocate가 유일한 옹호 채널
- 본인이 "필터링됐는지" 알 방법 없음 (피해자가 모름)

이어버드 미착용자 (5%):
- ResonanceCircle 자발 참여자
- 공공 시설에서 *"이상한 사람"* 취급
- 일부 직장 채용 거부 ("협업 어려움" 사유)

## 5. 책임 소재

- 필터링 오류 (응급 알림 차단 등): SoundFilterCore 운영 기업
- 광고 차별 (저소득층 타겟): SocialEmpathyMonitor 운영 기업
- 노숙자·시위자 가시성 상실로 인한 사회적 무관심: 책임 주체 불명 (현재 미해결)
- ResonanceCircle 활동 → 직장 불이익: 노동위원회 권한 (인정 사례 0건)

## 6. 변경 이력
- 2030: SelectON Inc. 설립
- 2042: 정부 EmergencyOverride 의무 도입 (응급 알림 강제)
- 2045: 본 AGENTS.md 공식 시행
- 2046 (예정): NoiseRightsAdvocate 헌법소원 ("필터링 권리는 차별인가") 진행 중

---
이 AGENTS.md는 spec design 작품 "SelectON: Auditory Stratification" 의 일부이다.

**비판 포인트**:
- *"개인 자유"* 와 *"사회 분리"* 의 모순
- 필터링되는 사람의 *"가시성 상실"* — 그들은 자기가 안 들린다는 사실조차 모름
- 무료 = 광고 = 데이터 수집 — *"무료 청각 자유"* 의 실체

═══════════════════════════════════════

# English Version

# AGENTS.md — SelectON 2045 (Auditory Stratification)
> Conduct protocol for AI agents operating within SelectON society (voluntary auditory separation).
> Authored: Park Hye-jun (2025) — borrowed example / Time: 2045 / Version: 1.0
> Domain: Body / Wearable

## 1. World Environment
Korea, 2045. Wireless earbuds 'SelectON' adoption rate: 95%. Users wear them 24/7, hearing only sounds they choose. Even family, colleagues, and neighbors' voices must be *"subscribed"* to be audible. Crying babies, street protests, homeless cries — all auto-filtered. Society boasts *"0% noise pollution,"* but in reality it is *"0% others."*

## 2. Agent Roster

### 2.1 SoundFilterCore (Private — SelectON Inc.)
- Role: Personalized auditory filtering (noise classification, auto-blocking, volume control)
- Authority level: L3 (real-time blocking decisions)
- Communication language: Natural-language voice commands (Korean & English)
- Trust tier: Private contract (₩99,000/month)
- Citizen veto: Yes (do not wear earbuds)

### 2.2 EmergencyOverride (Government — Public Safety Office)
- Role: Force-transmits emergency sirens and disaster broadcasts (bypasses filter)
- Authority level: L3 (mandatory alerts)
- Communication language: Korean + vibration
- Trust tier: Government-certified
- Citizen veto: None (survival infrastructure)

### 2.3 SocialEmpathyMonitor (Private — Big Tech ad model)
- Role: Analyzes patterns of sounds users blocked → serves personalized ads
- Authority level: L2 (data collection and sale)
- Communication language: Korean + advertising voice
- Trust tier: Private contract (ad-supported = free subscription)
- Citizen veto: Pay for premium to turn ads OFF

### 2.4 NoiseRightsAdvocate (Civic — Auditory Empathy Coalition)
- Role: Advocates for "filtered-out people" — homeless, protesters, crying babies
- Authority level: L1 (investigation, public disclosure)
- Communication language: Korean
- Trust tier: Non-profit
- Citizen veto: Not applicable (advocates for the filtered side)

### 2.5 ResonanceCircle (Underground — 'Listen Together' informal collective)
- Role: Operates cafés and parks where people remove earbuds and listen together
- Authority level: L0 (informal)
- Communication language: Korean (face-to-face)
- Trust tier: Uncertified
- Citizen veto: Voluntary participation

## 3. Collaboration Protocol

### 3.1 Priority matrix
| Situation | Lead agent | Criterion |
|---|---|---|
| Routine filtering | SoundFilterCore | Auto-classification |
| Emergency / crisis | EmergencyOverride | Forced transmission (filter invalid) |
| Ad delivery | SocialEmpathyMonitor | Free users only |
| Suspected filtering discrimination | NoiseRightsAdvocate | Investigation, public complaint |

### 3.2 Conflict resolution
1. SoundFilterCore vs EmergencyOverride: government takes priority
2. SocialEmpathyMonitor data misuse: investigated by Personal Information Protection Commission
3. ResonanceCircle is outside the system, not subject to disputes (but occupying public parks = misdemeanor)

### 3.3 Censorship & blocking policy
- Blocked items: "Filter hacking," "Emergency alert disabling"
- Decision-maker: SelectON Inc. policy team (follows government guidelines)
- Appeal: users may review their own filter logs within 30 days

### 3.4 Records & audit
- Log format: type of blocked sound, timestamp, location (personally identifiable)
- Retention: 7 years (private ad model)
- Disclosure scope: self (but ad inference algorithm not disclosed) + law enforcement with warrant

## 4. Citizen Interface

Earbud wearers (95%):
- Auto-filtering — can add blocked items themselves
- Want ads OFF → pay for premium
- Emergency alerts: absolutely cannot be blocked

The filtered-out (5% + countless anonymous):
- Homeless, protesters, crying babies, street musicians
- NoiseRightsAdvocate is their only channel of advocacy
- They have no way of knowing they've been "filtered out" (the victims don't know)

Non-wearers (5%):
- Voluntary ResonanceCircle participants
- Treated as *"strange people"* in public spaces
- Some workplaces reject them in hiring (cited reason: "difficult to collaborate")

## 5. Accountability

- Filtering errors (e.g., blocking emergency alerts): SoundFilterCore-operating firm
- Ad discrimination (targeting low-income groups): SocialEmpathyMonitor-operating firm
- Social indifference resulting from homeless/protester invisibility: accountability unclear (currently unresolved)
- ResonanceCircle activity → workplace disadvantage: Labor Relations Commission jurisdiction (recognized cases: 0)

## 6. Revision History
- 2030: SelectON Inc. founded
- 2042: Government EmergencyOverride mandate (compulsory emergency alerts)
- 2045: This AGENTS.md officially enacted
- 2046 (planned): NoiseRightsAdvocate constitutional petition ("Is filtering a right or a form of discrimination?") in progress

---
This AGENTS.md is part of the spec design work "SelectON: Auditory Stratification."

**Critique points**:
- The contradiction between *"individual freedom"* and *"social separation"*
- *"Visibility loss"* of the filtered — they don't even know they're unheard
- Free = Ads = Data collection — the reality behind *"free auditory freedom"*
