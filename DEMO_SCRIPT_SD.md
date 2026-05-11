# 라이브 데모 스크립트 — Speculative Design Council (Streamlit + Ollama)

> 워크숍 Hook 시연용 (압축 60초 ~ 5분).
> 청중이 **"4-에이전트 Council이 학생 narratype을 어떻게 다루는가"** 를 눈으로 확인할 수 있게 구성.

---

## 사전 점검 (데모 시작 30분 전)

- [ ] Ollama 서버 살아있음: `ollama list` 가 에러 없이 출력
- [ ] 모델 설치: `gemma4` (필수), `gemma4-mtp` (권장 — 3x 가속), `phi4-mini` (선택)
- [ ] `streamlit run app.py` 가 정상 시작되는지
- [ ] `.sessions/` 가 비어있거나 데모 세션만 (프로젝터에 무관한 과거 세션 안 보이게)
- [ ] 브라우저 줌 125%, 터미널 폰트 16pt+
- [ ] 인터넷 일부러 **꺼두기** (로컬이라는 것 시연 효과)
- [ ] 데모 narratype 텍스트 클립보드에 미리 복사 (HAPPY GATE — `templates.py` 의 `CONTEXT_PLACEHOLDER`)

---

## 60초 압축 시연 (워크숍 0-5분 Hook용)

### 0-15초 — "이게 진짜 일어나고 있는 일이다"

```bash
ollama list
```

> **말하기**: *"제 노트북에 깔린 AI들입니다. Gemma 4, deepseek, qwen3.5 — 인터넷 꺼도 다 돌아갑니다. 오늘 보여드릴 건 이 4개의 AI가 한 팀이 되어 여러분의 narratype을 같이 분석하는 모습이에요."*

(Wi-Fi 끄기 — `ping google.com` 으로 실증)

### 15-30초 — 앱 실행 + narratype 입력

```bash
streamlit run app.py
```

(브라우저 자동 오픈)

> **말하기**: *"이건 작년에 박지우 학생이 만든 narratype입니다 — 'HAPPY GATE: 웃지 않으면 출입 금지'."*

(클립보드에서 narratype 텍스트 paste)

### 30-50초 — Council 실행 라이브 (스트리밍)

[Council 실행] 버튼 클릭. 화면에:
- 🪞 거울 (Mirror) — 4 archetype 확장 시작
- 📍 지도 (Map) — 거울 비평 시작
- ⚖️ 의장 (Chairman) — 종합 시작

> **말하기 (스트리밍 동안)**: *"같은 narratype을 4가지 미래로 확장합니다 — 성장, 붕괴, 지속, 변혁. 이게 미래학자 Jim Dator의 4 futures archetypes입니다. 그리고 각 AI가 다른 역할을 맡고 — 이게 LLM Council 패턴이에요."*

### 50-60초 — 결과 + 메시지

(의장 종합이 끝나면, 4 archetype별 narratype + Constellation 좌표 보임)

> **말하기**: *"이게 한 학생 작품에 대한 4-에이전트의 deliberation입니다. 같은 코드, 다른 프롬프트로 — 우리가 오늘 워크숍에서 같이 디자인할 건 이런 'AI 사회'의 protocol입니다. AGENTS.md라고 부르는 진짜 표준이에요."*

(다음 슬라이드로 넘어가며) → 워크숍 본격 시작

---

## 5분 확장 시연 (시연용 슬롯이 더 있을 때)

위 60초 시연 후:

### 1분 추가 — Stage 2 (AGENTS.md 작성) 시연

> **말하기**: *"이제 이 narratype 세계용 AGENTS.md를 만들어볼까요?"*

[다음 단계로] 클릭 → Stage 2 자동 진행 → AGENTS.md markdown 출력 보여주기

### 1분 추가 — Export 시연

[산출물 생성] → "AGENTS.md" 선택 → 다운로드 버튼

> **말하기**: *"이걸 학생이 자기 spec design 작품에 그대로 첨부할 수 있어요. 진짜 markdown 파일로요."*

### 1분 추가 — 미래학자 모드

사이드바에서 [🔮 미래학자 모드] 토글 → Council 재실행

> **말하기**: *"이건 선택 옵션 — Dator 4 archetypes lens로 학생에게 메타 질문 10개를 던져요. '네가 가장 회피하고 있는 질문은?' 같은 거."*

### 1분 추가 — Persona Council 모드 (Option D, 가장 강렬한 시연)

사이드바 [Council 구성] 섹션 → Nemotron 30명 Excel 업로드 → [🤖 AI 추천 Council 구성] 클릭

(잠시 후 4명의 페르소나가 4 역할에 자동 매핑됨)
- 거울 역: 전기태 (74세 남, 광주 하역 노동자)
- 지도 역: 최은지 (71세 여, 서초 회계 사무원)
- 의장 역: ...
- 미래학자 역: ...

[✅ Council 모드 활성화] 체크 후 → Council 재실행

> **말하기**: *"이제 같은 narratype에 다른 사람들이 위원회를 구성합니다. 추상적 'Critic'이 아니라 실제 광주 70대 노동자가 1인칭으로 발언해요. 같은 코드, 다른 페르소나 — 결과가 어떻게 달라지는지 보세요."*

(거울 출력 시작) — *"전기태입니다. 광주 서구에서 하역 일 30년 했습니다. 이 HAPPY GATE 보니까..."*

### 1분 추가 — 학생들이 직접 시도해볼 수 있다는 메시지

> **말하기**: *"이 도구는 GitHub에 공개됩니다. 워크숍 끝나고 자기 narratype에 직접 돌려보세요. 비행기 모드에서도 작동하고, 데이터는 노트북 밖으로 안 나갑니다."*

---

## 학생 자율 활용용 5분 가이드 (워크숍 후 배포)

```
1. https://ollama.com 에서 Ollama 설치 (Mac/Win/Linux)
2. 터미널에서:
   ollama pull gemma4
   ollama pull gemma4-mtp  # 3x 가속 (선택)
3. GitHub에서 streamlit_spec_design_council 다운로드
4. cd streamlit_spec_design_council && pip install -r requirements.txt
5. streamlit run app.py
6. 자기 narratype 200-400자 입력 → Council 실행
7. AGENTS.md export → 자기 작품에 첨부
```

문제 시 README.md "문제 해결" 섹션 참조.

---

## 시연 중 주의

- **Ollama 첫 호출은 모델 로드 대기 5-10초** — 한번 실행해두면 빠름. 시연 전 미리 한 번 돌려서 warm-up
- **거울/지도/의장 출력이 길게 나옴** — 첫 1-2 문장만 읽고 다음으로 넘어가도 OK
- **인터넷 꺼두는 시연**은 의외로 강렬 — "진짜 로컬"임을 체감
- **MTP 모델 사용 시 속도 차이가 명확함** — 가능하면 MTP로 시연

---

## 백업 (Ollama 안 켜졌을 때)

미리 녹화한 30초 영상을 준비. 또는 `templates.py` 의 `DEMO_INPUTS` 를 활용한 캐시된 출력 보여주기.

가장 좋은 백업: **데모 실패 자체를 페다고지 재료로**. *"보세요, AI는 이렇게 자주 실패합니다. 그게 spec design 재료가 됩니다."*
