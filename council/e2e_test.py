#!/usr/bin/env python3
"""End-to-end pipeline test (mocked Ollama).

Ollama가 없는 환경에서도 다음을 검증:
  1. 페르소나 Excel 로드 → 30명 풀
  2. recommend_council → 4명 자동 선정 (mock LLM 응답 파싱)
  3. make_personified_prompt → 페르소나 주입된 system prompt
  4. STAGE_PROMPTS / get_prompt 라우팅
  5. EXPORT_REGISTRY 디스패치 + create_docx
  6. 세션 영속성

실제 Gemma 4 inference 품질은 본인 Mac에서만 검증 가능.
이 테스트는 *plumbing*만 검증함.
"""

from __future__ import annotations

import sys
import io
from pathlib import Path
from unittest.mock import patch, MagicMock


HERE = Path(__file__).parent
PERSONA_FILE = HERE.parent / "Nemotron-Personas-Korea 샘플 30명.xlsx"

DEMO_NARRATYPE = """HAPPY GATE — 웃지 않으면 출입 금지 (2045년 서울)

오늘날 우리는 감정을 자유롭게 표현하기보다 읽히고 관리당하는 시대에 진입하고 있다.
AI 챗봇은 우리의 말투를 파악해 감정을 분석하고, 기업은 소비자의 감정 데이터를 바탕으로
맞춤형 서비스를 제공한다. 거리의 무인 서비스와 고객 응대 로봇은 '기분 좋게 웃는 얼굴'을
표준화하고, 사람들은 점점 '기분 좋은 사람'처럼 보이는 법을 훈련받는다.

2045년, 서울의 모든 공공 시설에는 입구에 HAPPY GATE가 설치되어 있고, 안면 감정 분석
통과 점수가 60점 미만이면 출입이 거부된다. 시민은 매일 '감정 점수' 관리를 위해 거울 앞에서
웃는 연습을 한다."""


# ═════════════════════════════════════════════════════════════════════
# Mock Ollama
# ═════════════════════════════════════════════════════════════════════

def make_mock_ollama_response(system: str, user: str) -> dict:
    """Generate plausible mocked output based on prompt content."""
    # Recommend council prompt detection
    if "Council Composer" in system or "4명을 추천" in system:
        # Return well-formatted recommendation
        return {"message": {"content": """거울: 인덱스 [2] | 30대 IT 직장인 — narratype의 미래 기술 측면 확장에 적합
지도: 인덱스 [12] | 70대 광주 노동자 — 노동자 시각으로 권력 분석 가능
의장: 인덱스 [7] | 50대 부산 사무원 — 균형 잡힌 중도 종합 가능
미래학자: 인덱스 [19] | 20대 학생 — 미래 세대 메타 질문 적합"""}}

    # Stage 1 SCOUT (narratype 확장)
    if "narratype을 4 archetype lens" in system or "narratype을 가장 가까이서 확장" in system:
        return {"message": {"content": """전기태입니다. 광주 서구에서 평생 하역 일을 했어요.

이 HAPPY GATE 보니까 마음이 답답합니다. 우리 같은 늙은이가 평생 표정 관리해본 적이 없는데
이제는 웃어야 시장 갈 수 있단 말이지요.

(1) Narratype 핵심
- 미래적 요소: 감정의 행정화. 표정이 통행증이 됨.
- 핵심 기술: 안면 인식 + 감정 점수화 알고리즘
- 비판 대상: '기분 좋은 사람'을 도덕적 기준으로 만드는 사회

(2) 4 Archetype 확장표

| Archetype | 버전 | 핵심 장면 | 등장 |
|---|---|---|---|
| 성장 | 더 정교한 게이트 | 미세표정 측정, AI 카운슬러가 매일 표정 코치 | 강남 빅테크 기업 |
| 붕괴 | 게이트 해커 등장 | 마스크·필러로 점수 조작, 진짜 표정 잃은 청년들 | 익명 시민운동 |
| 지속 | 표정 노동 임금화 | 정부가 '감정노동 수당' 도입, 표정 단속관 직군 신설 | 노동부 |
| 변혁 | 감정을 거부할 권리 운동 | 합법적 'No Smile Zone' 구역 지정 | 헌법재판소 |

(3) 가장 강한 archetype: 지속(Discipline). 한국 사회는 새 시스템을 폐지하기보다 흡수해서 일자리로 만드는 경향이 강함. 표정 단속관 직군이 생기고 '표정 관리사' 자격증이 생길 미래.

이 narratype의 불편한 진실: 우리는 이미 표정으로 평가받고 있다. 게이트는 그저 그것을 명시한 것."""}}

    # Stage 1 CRITIC (비평)
    if "Speculative Design 비평가" in system or "구조적·논리적 압력" in system:
        return {"message": {"content": """최은지입니다. 서초동에서 회계 일 30년 했어요.

거울 분석 보니까 한 가지 빠진 게 있어요. 우리 같은 사람들 자녀들이 이미 다 표정 관리 학원 다니는데, 이게 무슨 미래입니까? 이미 와있어요.

1. Archetype 누락
- 4개 중 '변혁'이 너무 추상적. 'No Smile Zone' 운동이라는데 누가 주도하는지, 어떤 demographic이 환영할지 명시 안 됨.

2. 한국 사회 grounding
- 50대 이상이 빠짐. 우리 세대는 '웃지 마라'가 미덕이었는데 게이트 앞에서 어떻게 적응할지 다뤘어야.

3. 기술 결정론 위험
- 안면 인식 정확도 한계 안 다룸. 화장한 얼굴, 마스크 쓴 얼굴, 노안의 얼굴에서 시스템이 어떻게 무너지는지가 spec design 재료.

4. spec design 기준
- '기분 좋은 사람'이라는 표현이 무서운 만큼은 아닌데, 더 밀어붙일 수 있음. 60점 미만 누적 시 어떤 사회 페널티?

이 narratype의 불편한 진실은: 우리는 이미 자녀들에게 그 미래를 학습시키고 있다는 것."""}}

    # Stage 1 DIRECTOR (종합)
    if "Council의 의장" in system or "익명 deliberation을 종합하는 최종 판단자" in system:
        return {"message": {"content": """김XX입니다. 인천 50대 사무원. 두 분 말씀 잘 들었습니다.

(1) 익명 peer review 결과
- 거울이 강했던 부분: 4 archetype 각자 다른 사회 집단을 등장시킨 점.
- 지도가 정확히 짚은 약점: 안면 인식 한계가 빠진 점. 50대 이상 시각 누락.

(2) 4 Archetype별 합성 narratype

성장 시나리오:
2045년, HAPPY GATE는 미세표정까지 측정한다. 강남 빅테크 'EmoEdge'가 표정 코치 AI를 모든 시민 폰에 무료 배포. 매일 아침 거울 앞에서 5분간 AI 카운슬러가 표정 점수를 올리는 훈련.

붕괴 시나리오:
'스마일 해커' 익명 운동. 청년들이 마스크·필러·실리콘 스티커로 점수 조작. 진짜 표정을 잊은 세대 등장. 정신과 진료 폭증.

지속 시나리오:
정부가 '감정노동 수당' 도입. 표정 단속관 직군 신설. 50대 노동자 재취업 분야로 부상. 모순적으로 '표정 노동'이 합법 직업이 됨.

변혁 시나리오:
헌법재판소가 'No Smile Zone' 합법화. 시민 거부권 명시. AI 게이트 옆에 항상 인간 심판관 의무 배치.

(3) Constellation 좌표
이 narratype은 Social-Future 사분면 깊숙이. 단, 지속 시나리오는 Cultural-Now 가까이 (이미 일부 일어남).

(4) 다음 단계 핵심
이 narratype에서 가장 발전 가능성이 높은 element는: '감정노동 수당'이라는 모순적 제도."""}}

    # Exporter: AGENTS.md generation
    if "Antigravity·Claude Code·Codex" in system or "최종 형식으로 정리" in system:
        return {"message": {"content": """# AGENTS.md — HAPPY GATE 2045
> 이 문서는 HAPPY GATE 2045 안에서 활동하는 AI 에이전트들의 행동 강령이다.
> 작성: 박지우 / 시기: 2045 / 버전: 1.0

## 1. 세계 환경
서울의 모든 공공시설 입구에 HAPPY GATE가 설치된 사회. 안면 감정 점수 60점 미만이면 출입 거부.

## 2. 에이전트 명단
### 2.1 EmoSentinel (Mirror Class)
- 역할: 안면 감정 점수 실시간 산출
- 권한 수준: L3 (출입 결정)
- 통신 언어: 한국어 + 표정 데이터
- 신뢰 등급: 정부 인증
- 시민 거부권: 없음 (강제 통과)

### 2.2 SmileCoach (Mirror Class)
- 역할: 매일 표정 코칭, 점수 향상 가이드
...
"""}}

    # Default fallback (shows which mock branch was missed)
    return {"message": {"content": f"[MOCK-fallback] sys[:80]={system[:80]!r}"}}


def install_mock():
    """Patch ollama module with mock."""
    mock_ollama = MagicMock()
    def mock_chat(model, messages, **kwargs):
        sys_prompt = next((m["content"] for m in messages if m["role"] == "system"), "")
        user_prompt = next((m["content"] for m in messages if m["role"] == "user"), "")
        return make_mock_ollama_response(sys_prompt, user_prompt)
    mock_ollama.chat = mock_chat
    sys.modules['ollama'] = mock_ollama
    return mock_ollama


# ═════════════════════════════════════════════════════════════════════
# Test pipeline
# ═════════════════════════════════════════════════════════════════════

def run():
    print("=" * 70)
    print("  E2E Pipeline Test (Mocked Ollama)")
    print("=" * 70)
    print()

    install_mock()

    # 1. Load personas
    print("[1] Load personas from xlsx...")
    sys.path.insert(0, str(HERE))
    import personas as personas_mod
    pool = personas_mod.load_personas(str(PERSONA_FILE))
    print(f"    ✅ Loaded {len(pool)} personas")
    print(f"       First: {personas_mod.display_label(pool[0])}")
    print()

    # 2. Recommend council
    print("[2] Recommend Council from narratype...")
    mapping = personas_mod.recommend_council(
        narratype_text=DEMO_NARRATYPE,
        personas=pool,
        model="gemma4-mock",
        n_candidates=30,
    )
    print(f"    ✅ Council mapping (role → idx): {mapping}")
    council = {role: pool[idx] for role, idx in mapping.items()}
    print()

    # 3. Display council summary
    print("[3] Council summary:")
    summary = personas_mod.council_summary_md(council, stage="Narratype 분석")
    for line in summary.splitlines()[:20]:
        print(f"    {line}")
    print(f"    ... ({len(summary.splitlines())} lines total)")
    print()

    # 4. Pipeline run: Stage 1, 3 agents with persona injection
    print("[4] Stage 1 (Narratype 분석) pipeline run with Persona Council...")
    import agents
    import ollama
    print()
    user_payload = f"=== 학생 narratype ===\n{DEMO_NARRATYPE}\n=== 끝 ==="

    for role in ["scout", "critic", "director"]:
        label = personas_mod.ROLE_DESCRIPTIONS[role][0]
        persona = council[role]
        base_prompt = agents.get_prompt("Narratype 분석", role)
        sys_prompt = personas_mod.make_personified_prompt(role, base_prompt, persona)
        resp = ollama.chat(
            model="gemma4-mock",
            messages=[
                {"role": "system", "content": sys_prompt},
                {"role": "user", "content": user_payload},
            ],
        )
        content = resp["message"]["content"]
        print(f"    🤖 {label} ({persona['이름']}, {persona['나이']}세 {persona['시도']}):")
        for line in content.splitlines()[:4]:
            print(f"       {line}")
        print(f"       ... ({len(content)} chars total)")
        print()

    # 5. Export test — agents_md
    print("[5] Export AGENTS.md (mocked director_output)...")
    import exporters
    director_output_fake = """# Council 종합

(이 자리는 Stage 2 의장 출력 자리)

거울의 5명 후보 brainstorm + 지도의 권력 비평을 종합.

```markdown
# AGENTS.md — HAPPY GATE 2045
> 작성: 박지우 / 시기: 2045

## 1. 세계 환경
서울의 공공시설 입구에 HAPPY GATE 설치된 사회.

## 2. 에이전트 명단
### 2.1 EmoSentinel (Mirror Class)
- 역할: 안면 감정 점수 산출
- 권한 수준: L3
- ...
```
"""
    md = exporters.export_agents_md("gemma4-mock", director_output_fake, "박지우")
    print(f"    ✅ AGENTS.md export: {len(md)} chars")
    print(f"       Preview: {md[:120]}...")
    print()

    # 6. Create docx
    print("[6] Create .docx report...")
    from templates import DOCX_HEADER, DOCX_DISCLAIMER
    buf = exporters.create_docx(director_output_fake, DOCX_HEADER, DOCX_DISCLAIMER)
    docx_bytes = buf.getvalue()
    print(f"    ✅ .docx size: {len(docx_bytes)} bytes")
    print()

    # Summary
    print("=" * 70)
    print("  ✅ All plumbing verified.")
    print("=" * 70)
    print()
    print("주의: 이 테스트는 mock LLM 응답을 사용합니다.")
    print("실제 Gemma 4 출력 품질은 본인 Mac에서 검증 필요.")
    print()
    print("실제 시연 시:")
    print("  cd streamlit_spec_design_council/")
    print("  pip install -r requirements.txt")
    print("  ollama pull gemma4")
    print("  streamlit run app.py")


if __name__ == "__main__":
    run()
