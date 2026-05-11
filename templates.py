"""Speculative Design Council — 입력 템플릿 + 단계별 체크리스트 + 내보내기 라벨.

원본: "나만의 연구팀" templates.py
변환: 연구 분야 → SD 작품 도메인. agents.py STAGE_PROMPTS의 key와 정확히 일치.
"""

# ═════════════════════════════════════════════════════════════════════
# 학생 narratype 도메인 (Yonsei SD 2026 클래스 기준)
# ═════════════════════════════════════════════════════════════════════

NARRATYPE_DOMAINS = [
    "감정·정서 (Emotion / Affect)",
    "노동·일상 (Labor / Everyday)",
    "신체·웨어러블 (Body / Wearable)",
    "정체성·관계 (Identity / Relationship)",
    "생태·환경 (Ecology / Environment)",
    "거버넌스·시민권 (Governance / Citizenship)",
    "AI·자동화 (AI / Automation)",
    "기타 (직접 입력)",
]

# agents.py STAGE_PROMPTS 의 key 와 정확히 일치해야 함
RESEARCH_STAGES = [
    "Narratype 분석",
    "AGENTS.md 작성",
    "청중 반응 시뮬레이션",
]

# 호환 alias (코드 다른 곳에서 RESEARCH_FIELDS 참조 시)
RESEARCH_FIELDS = NARRATYPE_DOMAINS

# ═════════════════════════════════════════════════════════════════════
# 단계별 필수 항목 체크리스트 (사이드바 참고용)
# ═════════════════════════════════════════════════════════════════════

REQUIRED_ITEMS = {
    "Narratype 분석": [
        "narratype 도메인",
        "스펙 시나리오 핵심 단락 (200-400자)",
        "타겟 시점 (예: 2045년 한국)",
        "핵심 기술 1개 (시나리오의 트리거)",
        "비판하는 현재 사회 element 1개",
    ],
    "AGENTS.md 작성": [
        "Narratype 분석 결과 (이전 단계 자동 입력)",
        "이 세계의 핵심 갈등 1줄",
        "AI 에이전트가 다루는 주요 영역 (예: 신원/금융/감정/안전)",
        "(선택) 실세계 AGENTS.md 참고 사례 업로드",
    ],
    "청중 반응 시뮬레이션": [
        "narratype + AGENTS.md (이전 단계 자동 입력)",
        "Nemotron 페르소나 샘플 업로드 (Excel/JSON, 권장 30명)",
        "또는 학생 자가 인터뷰 페르소나 (선택)",
        "특별히 보고 싶은 demographic (선택)",
    ],
}

# ═════════════════════════════════════════════════════════════════════
# 맥락 입력 예시 (placeholder)
# ═════════════════════════════════════════════════════════════════════

CONTEXT_PLACEHOLDER = """예시 (2025년 박지우 학생 narratype 차용):

HAPPY GATE — 웃지 않으면 출입 금지 (2045년 서울)

오늘날 우리는 감정을 자유롭게 표현하기보다 읽히고 관리당하는 시대에 진입하고 있다.
AI 챗봇은 우리의 말투를 파악해 감정을 분석하고, 기업은 소비자의 감정 데이터를 바탕으로
맞춤형 서비스를 제공한다. 거리의 무인 서비스와 고객 응대 로봇은 '기분 좋게 웃는 얼굴'을
표준화하고, 사람들은 점점 '기분 좋은 사람'처럼 보이는 법을 훈련받는다.

2045년, 서울의 모든 공공 시설(지하철·버스·관공서·대형마트)에는 입구에 HAPPY GATE가 설치되어
있고, 안면 감정 분석 통과 점수가 60점 미만이면 출입이 거부된다.
시민은 매일 '감정 점수'를 관리하기 위해 거울 앞에서 웃는 연습을 한다."""

KEYWORDS_PLACEHOLDER = "예: 감정 검열, 안면 인식, 표정 노동, 공공 인프라"

EXTRA_PLACEHOLDER = """특별히 강조할 내용이나 제외할 조건이 있으면 적어주세요.

예: SF tropes(매트릭스/블랙미러)로 회귀하지 말 것 / 한국 사회 특수성 강조 /
지하철 시나리오만 다룰 것 / 청소년 시각 포함"""

RESOURCES_HELP = (
    "narratype 보조 자료 (선행 사례 PDF, 메모 .md, 텍스트 .txt) 를 업로드하세요. "
    "최대 5개. 업로드된 파일은 로컬 메모리에만 보관됩니다.  "
    "※ Persona 풀 (Nemotron Excel) 은 여기가 아니라 사이드바의 'Council 구성' 영역에서 업로드하세요."
)

PROJECT_NAME_PLACEHOLDER = "예: HAPPY_GATE_박지우 / MBTI_BAR_김OO / DOG_ROBOT_이OO"

# ═════════════════════════════════════════════════════════════════════
# Word 출력 구조
# ═════════════════════════════════════════════════════════════════════

DOCX_HEADER = "Speculative Design Council — 작품 분석 보고서"
DOCX_DISCLAIMER = (
    "본 문서는 AI(Ollama 로컬 Gemma 4 + 선택적 클라우드 LLM)가 작성한 분석입니다. "
    "Speculative Design은 정답이 아니라 질문을 만드는 작업이므로, "
    "AI 분석은 학생 본인의 작가적 결정을 대체하지 않습니다. "
    "'[추측]' 표시는 직접 검증하세요. 페르소나 반응은 합성 시뮬레이션입니다."
)

# ═════════════════════════════════════════════════════════════════════
# 산출물 내보내기 라벨 (UI 표시용 — 실제 디스패치는 exporters.EXPORT_REGISTRY)
# ═════════════════════════════════════════════════════════════════════

EXPORT_LABELS = {
    "docx": "Word 보고서 (.docx) — 최종 결과물 첨부용",
    "agents_md": "AGENTS.md (.md) — narratype 세계 protocol 문서",
    "constellation": "Constellation 좌표 (.txt) — STEEP 휠 + 4 archetype plot 데이터",
    "diptych_seed": "Living Diptych 시드 (.md) — Alt 1 결과물 우측 패널 초기값",
    "audience_report": "청중 반응 보고서 (.md) — 페르소나 반응 + demographic 분석",
}

# ═════════════════════════════════════════════════════════════════════
# 단계 설명 + 기대 결과물 (UI에서 사용자에게 보여줌)
# ═════════════════════════════════════════════════════════════════════

STAGE_DESCRIPTIONS = {
    "Narratype 분석": {
        "summary": "본인 시나리오를 4가지 미래 원형(성장·붕괴·지속·변혁)으로 확장합니다.",
        "input": "시나리오 핵심 단락 200-400자 (장소·시점·인물·기술 포함)",
        "output": "4 archetype별 narratype 확장 + Constellation 좌표 제안 + 다음 발전 element 1줄",
        "use_case": "첫 단계 권장. 본인 작품의 가능성 공간을 4 방향으로 펼치고 어디로 더 갈지 결정.",
    },
    "AGENTS.md 작성": {
        "summary": "시나리오 세계 안에서 활동할 AI 에이전트들의 협업 규칙(AGENTS.md)을 작성합니다.",
        "input": "Stage 1 결과 + 핵심 갈등 1줄 + AI가 다루는 영역 (신원/금융/감정/안전 등)",
        "output": "markdown 표준 AGENTS.md 파일 — 에이전트 5명, 권한·통신언어·검열규칙·시민 인터페이스",
        "use_case": "본인 작품에 'AI 거버넌스 문서'를 직접 첨부하고 싶을 때. 실제 IT 표준 적용.",
    },
    "청중 반응 시뮬레이션": {
        "summary": "Nemotron 페르소나 30명이 본인 작품에 반응하고 4 archetype 분포로 분석합니다.",
        "input": "Stage 1+2 결과 + Nemotron 페르소나 풀 (사이드바 업로드)",
        "output": "페르소나별 1인칭 반응 + 4 archetype 분포 (성장 X% / 붕괴 Y% / 지속 Z% / 변혁 W%) + demographic 사각지대 분석",
        "use_case": "2025년 '대중 반응 분석' 한계 극복용. 친구·가족 중심 동질 반응 → demographic 다양한 청중.",
    },
}

STAGE_DESCRIPTIONS_EN = {
    "Narratype 분석": {
        "summary": "Expand your scenario into Dator's Four Futures (Continued Growth · Collapse · Discipline · Transformation).",
        "input": "Scenario core paragraph 200-400 chars (place, time, characters, technology).",
        "output": "Narratype expanded into each of 4 archetypes + Constellation coordinate suggestion + 1-line next development element.",
        "use_case": "Recommended first stage. Open your work's possibility space in 4 directions, decide where to push further.",
    },
    "AGENTS.md 작성": {
        "summary": "Author an AGENTS.md (collaboration protocol for AI agents living in your scenario world).",
        "input": "Stage 1 output + core conflict (1 line) + AI domain (identity / finance / emotion / safety, etc.).",
        "output": "markdown-standard AGENTS.md file — 5 agents, authority levels, communication language, censorship rules, citizen interface.",
        "use_case": "When you want to attach a real 'AI governance document' to your spec design artifact. Uses the actual 2026 IT standard.",
    },
    "청중 반응 시뮬레이션": {
        "summary": "30 Nemotron personas react to your work; reactions classified into the 4 archetype distribution.",
        "input": "Stage 1+2 outputs + Nemotron persona pool (upload via sidebar).",
        "output": "Per-persona 1st-person reactions + 4 archetype distribution (Growth X% / Collapse Y% / Discipline Z% / Transformation W%) + demographic blind-spot analysis.",
        "use_case": "Overcomes 2025's 'public reaction analysis' limitation (friends-and-family homogeneous reactions → demographically diverse audience).",
    },
}

# ═════════════════════════════════════════════════════════════════════
# UI 다국어 (i18n) — 핵심 문자열만 토글
# ═════════════════════════════════════════════════════════════════════

UI_STRINGS = {
    "ko": {
        "lang_label": "언어 / Language",
        "lang_ko": "한국어",
        "lang_en": "English",
        "page_title": "Speculative Design Council",
        "masthead_sub": "Yonsei University · College of Human Ecology · 2026 Speculative Design",
        "masthead_desc": "4-에이전트 Council × 3 단계 = narratype 분석 / AGENTS.md 작성 / 청중 반응. 로컬 LLM 기반, 데이터 외부 전송 없음.",
        "onboarding_title": "사용 흐름 (처음이라면 여기부터)",
        "step1": "narratype 핵심 단락 작성 — 아래 '맥락' 입력란, 200-400자",
        "step2": "(선택) Persona Council 구성 — 사이드바에 Excel 업로드 → AI 추천 → Council 모드 ON",
        "step3": "[Council 실행] 버튼 클릭 — 거울→지도→의장 순차 진행 후 산출물 다운로드",
        "details_summary": "용어 + 더 자세히 (펼치기)",
        "disclaimer": "본 도구의 출력은 AI가 생성한 초안이며 학생의 작가적 결정을 대체하지 않습니다. Persona Council 응답은 합성 페르소나 기반 시뮬레이션입니다 (실제 사람 의견 아님). 업로드 파일은 로컬 메모리에만 보관되며 외부로 전송되지 않습니다.",
        "project_label": "프로젝트",
        "example_load": "예시 로드",
        "example_help": "선택한 2025 학생 narratype을 자동 입력합니다.",
        "narratype_resources": "narratype 보조 자료 (선택 · PDF / MD / TXT)",
        "resources_caption": "⚠ Persona 풀 (Nemotron Excel) 은 여기가 아니라 사이드바 → Council 구성 에서 업로드하세요.",
        "context_input_label": "narratype 맥락",
        "context_input_help": "장소·시점·인물·기술을 모두 포함해 200-400자로 작성하세요.",
        "stage_label": "단계",
        "council_run": "Council 실행",
        "council_compose": "Council 구성 (선택)",
        "council_compose_caption": "Nemotron-Personas-Korea Excel/JSON을 올리면, 추상 Council 대신 실제 demographic 페르소나가 거울/지도/의장/미래학자 역할을 연기합니다.",
        "ai_recommend_council": "AI 추천 Council 구성",
        "council_mode_on": "Council 모드 활성화",
        "council_reset": "Council 다시 구성",
        "advisor_mode": "미래학자 모드 (4번째 에이전트)",
        "thinking_mode": "사고 모드 (thinking)",
        "n_rounds_label": "Council 라운드 수",
        "model_label": "모델 (작은 순)",
        "advisor_model": "└ 미래학자 모델",
        "stage_box_does": "이 단계가 하는 일:",
        "stage_box_input": "입력:",
        "stage_box_output": "기대 결과물:",
        "stage_box_when": "언제 쓰나?",
    },
    "en": {
        "lang_label": "언어 / Language",
        "lang_ko": "한국어",
        "lang_en": "English",
        "page_title": "Speculative Design Council",
        "masthead_sub": "Yonsei University · College of Human Ecology · 2026 Speculative Design",
        "masthead_desc": "4-agent Council × 3 stages = narratype analysis / AGENTS.md authoring / audience reaction. Powered by local LLM, no data leaves your machine.",
        "onboarding_title": "How to use (start here if it's your first time)",
        "step1": "Write your narratype core paragraph — see the 'context' input below, 200-400 chars",
        "step2": "(Optional) Compose a Persona Council — upload Excel in sidebar → AI recommend → enable Council mode",
        "step3": "Click [Run Council] — Mirror → Map → Chairman runs sequentially, then download artifacts",
        "details_summary": "Glossary + Details (expand)",
        "disclaimer": "Outputs are AI-generated drafts and do not replace your authorial decisions. Persona Council responses are synthetic-persona simulations (not real human opinions). Uploaded files are stored only in local memory and never transmitted externally.",
        "project_label": "Project",
        "example_load": "Load example",
        "example_help": "Loads the selected 2025 student narratype automatically.",
        "narratype_resources": "Narratype supporting materials (optional · PDF / MD / TXT)",
        "resources_caption": "⚠ Persona pool (Nemotron Excel) is NOT uploaded here — use the sidebar → Council Composition section.",
        "context_input_label": "Narratype context",
        "context_input_help": "Write 200-400 chars including place, time, characters, and technology.",
        "stage_label": "Stage",
        "council_run": "Run Council",
        "council_compose": "Council Composition (optional)",
        "council_compose_caption": "Upload a Nemotron-Personas-Korea Excel/JSON file: real demographic personas will play the Mirror/Map/Chairman/Futurist roles instead of the abstract Council.",
        "ai_recommend_council": "AI-Recommend Council",
        "council_mode_on": "Activate Council Mode",
        "council_reset": "Re-compose Council",
        "advisor_mode": "Futurist Mode (4th agent)",
        "thinking_mode": "Thinking Mode",
        "n_rounds_label": "Council Rounds",
        "model_label": "Model (smallest first)",
        "advisor_model": "└ Futurist model",
        "stage_box_does": "What this stage does:",
        "stage_box_input": "Input:",
        "stage_box_output": "Expected output:",
        "stage_box_when": "When to use it?",
    },
}


def tr(key: str, lang: str = "ko") -> str:
    """Translate UI key. Falls back to Korean if key missing in selected lang."""
    return UI_STRINGS.get(lang, UI_STRINGS["ko"]).get(key, UI_STRINGS["ko"].get(key, key))

# narratype = 본 수업 박은선 교수님 사용 용어 (narrative + archetype).
# 미래 시나리오 + 거주 인물 + 세계관의 결합 단위.
GLOSSARY = {
    "narratype": "본 수업의 핵심 작업 단위. 미래 시나리오 + 거주 인물 + 세계관의 결합. (narrative + archetype 의 portmanteau로 추정. 박은선 교수님 수업 자료 출처.)",
    "Dator 4 archetypes": "Jim Dator(미래학자)의 4가지 미래 원형. 성장(Continued Growth) · 붕괴(Collapse) · 지속(Discipline) · 변혁(Transformation).",
    "AGENTS.md": "Anthropic·Google·OpenAI 협업 AI 도구가 사용하는 markdown 표준. 에이전트 역할·권한·통신 규칙을 명시하는 파일.",
    "Constellation": "학생 작품의 archetype 분포를 STEEP 휠 위에 plot한 시각화. 클래스 전체 = 별자리.",
    "Persona Council": "추상적 거울/지도/의장 대신 Nemotron 페르소나 4명이 1인칭으로 Council 역할을 연기.",
}

# ═════════════════════════════════════════════════════════════════════
# 데모 시나리오 (Hook 시연용 + smoke_test에서 활용)
# ═════════════════════════════════════════════════════════════════════

DEMO_PROJECT_NAME = "HAPPY_GATE_demo"

# Default demo (backward compat)
DEMO_INPUTS = {
    "field": "감정·정서 (Emotion / Affect)",
    "stage": "Narratype 분석",
    "context": CONTEXT_PLACEHOLDER,
    "keywords": "감정 검열, 안면 인식, 표정 노동, 공공 인프라",
    "extra": "한국 사회 특수성 강조, SF tropes 회피",
}

# 4가지 데모 시나리오 (2025 학생 narratype 차용)
DEMO_SCENARIOS = {
    "happy_gate": {
        "label": "박지우 — HAPPY GATE (감정 검열)",
        "project_name": "HAPPY_GATE_박지우",
        "field": "감정·정서 (Emotion / Affect)",
        "stage": "Narratype 분석",
        "context": """HAPPY GATE — 웃지 않으면 출입 금지 (2045년 서울)

오늘날 우리는 감정을 자유롭게 표현하기보다 읽히고 관리당하는 시대에 진입하고 있다.
AI 챗봇은 우리의 말투를 파악해 감정을 분석하고, 기업은 소비자의 감정 데이터를 바탕으로
맞춤형 서비스를 제공한다. 거리의 무인 서비스와 고객 응대 로봇은 '기분 좋게 웃는 얼굴'을
표준화하고, 사람들은 점점 '기분 좋은 사람'처럼 보이는 법을 훈련받는다.

2045년, 서울의 모든 공공 시설(지하철·버스·관공서·대형마트)에는 입구에 HAPPY GATE가 설치되어
있고, 안면 감정 분석 통과 점수가 60점 미만이면 출입이 거부된다.
시민은 매일 '감정 점수'를 관리하기 위해 거울 앞에서 웃는 연습을 한다.""",
        "keywords": "감정 검열, 안면 인식, 표정 노동, 공공 인프라",
        "extra": "한국 사회 특수성 강조, SF tropes 회피",
    },
    "cocoo": {
        "label": "이예진 — COCOO (자녀 CCTV 구독제)",
        "project_name": "COCOO_이예진",
        "field": "정체성·관계 (Identity / Relationship)",
        "stage": "Narratype 분석",
        "context": """COCOO — Invisible Safety Net (2045년 한국)

자녀 안전에 대한 부모의 불안이 산업화된 사회. 정부와 민간 기업이 협업해 만든
'COCOO' 서비스는 자녀 안전 관리 시스템으로 자리잡았다. 학교·학원·놀이터·길거리
모든 곳에 설치된 공공 CCTV망에 부모가 월 구독료를 내면 자녀 영상 24시간 접근 가능.

자녀에게 웨어러블 감지 기기(목걸이·시계 형태)를 장착하면 위치·심박·표정·음성이
실시간 부모 앱으로 전송된다. 처음엔 안전 명목이었으나, 점차 '학습 효율 분석',
'친구 관계 평가', '미래 성공 가능성 예측' 같은 부가 서비스로 확장. 자녀가 사춘기에
"보고 싶지 않다"고 외치면 부모가 항의하여 '정부 정책 시정 요구'로 번진다.""",
        "keywords": "CCTV 구독제, 자녀 감시, 웨어러블, 부모 불안 산업",
        "extra": "자녀의 거부권, 정부-기업 결탁 구조 강조",
    },
    "split": {
        "label": "심영석 — SPLIT (기후 불평등)",
        "project_name": "SPLIT_심영석",
        "field": "생태·환경 (Ecology / Environment)",
        "stage": "Narratype 분석",
        "context": """SPLIT — 기후 위기의 정상화 (2045년 한국)

기후 위기가 일상이 된 사회. 폭염·홍수·산불·미세먼지가 연중 반복되지만, 시민들은
'이제 그러려니' 한다. 단, 기후 위기의 '영향'은 계급에 따라 극명하게 분리(SPLIT)된다.

상위 10%는 실내 정수·필터·항온·항습 인프라가 갖춰진 'Bubble Towers'에 거주.
지하철역에 직결되어 외부 공기를 마실 일이 없다. 중산층은 마스크·청정기·환기시스템
3종 세트로 버틴다. 하위 30%는 '기후 노동자' — 폭염 속 배달, 강풍 속 건설, 미세먼지
속 청소를 담당. 평균 수명이 상위 계급보다 12년 짧지만 이 격차는 '개인의 직업 선택'
으로 설명된다.""",
        "keywords": "기후 정상화, 계급 분리, 기후 노동자, Bubble Towers",
        "extra": "계급별 신체적 영향 격차, '정상화'의 폭력성 강조",
    },
    "selecton": {
        "label": "박혜준 — SelectON (이어버드 사회 단절)",
        "project_name": "SelectON_박혜준",
        "field": "신체·웨어러블 (Body / Wearable)",
        "stage": "Narratype 분석",
        "context": """SelectON — 자발적 청각 분리 사회 (2045년 한국)

2016년 에어팟 출시 이후 무선 이어버드는 일상 인프라가 되었다. 2045년 현재
'SelectON' 이어버드는 한국인 95%가 24시간 착용 중. 사용자는 듣고 싶은 소리만
선택(Select-On)할 수 있다. 가족·동료·이웃의 목소리도 '구독' 해야 들린다.

지하철·버스·카페·식당 어디서나 사람들이 같은 공간에 있지만 각자 다른 청각
세계에 산다. 우는 아기 소리도, 노숙자의 외침도, 거리 시위 구호도 모두 자동
필터링. '소음 공해 0%'을 자랑하지만 실은 '타인 0%' 사회. 청각 분리는 결국
공감 분리로 이어진다.""",
        "keywords": "이어버드, 청각 분리, 소음 필터링, 공감 상실",
        "extra": "공공 공간에서의 사적 분리, 청각 정치학 강조",
    },
}

DEMO_RESOURCE_PATH = ""  # 사전 자료 없이 시연 가능
DEMO_RESOURCE_FILENAME = ""

# ═════════════════════════════════════════════════════════════════════
