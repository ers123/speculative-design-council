# Workshop Backup Plan — 진행자용 체크리스트

> 워크숍 당일 발생 가능한 실패 시나리오 + 대응책.
> 진행자(HarmonyOn + 박은선 교수님) 공유용.
>
> **핵심 전제**: Streamlit Council 설치는 학생 선택사항. **HarmonyOn 노트북 1대가 메인 데모 장비**. 학생 대다수는 폰 + 브라우저 + 종이로 참여한다고 가정.

---

## 사전 준비물 (워크숍 1주 전 확보)

| # | 항목 | 누가 | 상태 |
|---|---|---|---|
| 1 | **HarmonyOn 노트북 = 메인 시연 장비** (Ollama·Gemma 4 E2B+E4B 미리 로드) | HarmonyOn | [ ] |
| 2 | 사전 녹화 데모 영상 (60초) — Council 한 라운드 정상 작동 (Ollama 죽었을 때 fallback) | HarmonyOn | [ ] |
| 3 | 페르소나 카드 인쇄본 (10명 또는 30명) — 종이 fallback | HarmonyOn | [ ] |
| 4 | AGENTS.md 4 도메인 예시 (HAPPY GATE / COCOO / SPLIT / SelectON) — repo `examples/` | HarmonyOn (인쇄 또는 학생에 URL 공유) | [ ] |
| 5 | 학생 narratype worksheet 인쇄본 | 교수님 (수업 자료 출력) | [ ] |
| 6 | 프로젝터 HDMI 어댑터 + USB stick에 코드·영상 백업 | HarmonyOn | [ ] |

---

## 실패 시나리오 + 대응

### 시나리오 1 — **HarmonyOn 노트북 Ollama가 안 켜짐** (가장 큰 리스크)
**증상**: 시연 중 `streamlit run app.py` → "Could not connect to ollama server"
**즉시 대응**:
1. 별도 터미널 창에서 `ollama serve` 다시 실행
2. 그래도 안 되면 → **사전 녹화 데모 영상 (USB)** 프로젝터로 재생
3. 영상 보면서 *"이런 식으로 도구가 작동한다"* 설명 + 학생은 폰·브라우저 활동에 집중

### 시나리오 2 — 학생 폰 Edge Gallery 호환 안 됨
**증상**: iOS<17, 구형 Android, 저장 공간 부족
**즉시 대응**:
1. 옆 학생 폰 일시 공유 (Mirror 활동만 함께)
2. 또는 narratype 작성·AGENTS.md 작성에 집중하고 Mirror 부분은 짝꿍 페어링

### 시나리오 3 — 시연 도중 Gemma 4 응답 너무 느림 (>30초)
**증상**: 거울 응답이 30초 넘게 안 나오거나 첫 토큰까지 1분 이상
**즉시 대응**:
1. 사이드바 모델 영역 → **가장 작은 모델 (E2B)** 선택 (가장 위)
2. 사고 모드 (thinking) **OFF**
3. 다른 무거운 앱 (Chrome 탭, Slack 등) 종료
4. 그래도 느리면 → 사전 녹화 영상으로 전환

### 시나리오 4 — 강의실 wifi 끊김 / 클라우드 LLM 차단
**증상**: ChatGPT/Claude 페이지 안 열림 (학생 노트북 브라우저)
**즉시 대응**:
1. Telephone Round의 "Map" 단계를 *"오프라인 토론"* 으로 변형 — 짝꿍과 직접 대화로 narratype 다듬기
2. HarmonyOn 노트북 Streamlit Council은 로컬이라 wifi 무관 — 시연은 정상 진행

### 시나리오 5 — Streamlit app 크래시 / 멈춤 (HarmonyOn 노트북)
**증상**: 브라우저 탭에 "Connection lost" 또는 응답 없음
**즉시 대응**:
1. 브라우저 새로고침 (F5) — 세션 자동 복구
2. 안 되면 터미널 Ctrl+C → `streamlit run app.py` 다시 실행 (15초)
3. 그동안 학생들에게 narratype 짝꿍 review 시간 부여 (시간 손실 0)

### 시나리오 6 — 학생 narratype 미준비
**증상**: 학생이 본인 시나리오 못 작성, 시간 부족
**즉시 대응**:
1. **[예시 로드] 버튼** → 데모 시나리오 4종 중 하나 선택해서 시연
2. 학생은 4개 도메인 예시 (HAPPY GATE 등) 중 본인 분야와 가까운 것 골라 *"이것 출발점으로 본인 작품에 어떻게 적용할지"* 메모
3. NARRATYPE_WORKSHEET 인쇄본을 워크숍 중 5분 작성

### 시나리오 7 — 일부 학생이 설치 시도했는데 실패
**증상**: STUDENT_PREP 도전 트랙으로 Streamlit 설치 시도한 학생이 *"안 돌아가요"*
**즉시 대응**:
1. **워크숍 30분 일찍 도착한 학생** → HarmonyOn 1:1 트러블슈팅
2. 워크숍 시작 후 발견 시 → *"괜찮아요, 오늘은 제 노트북 보면 됩니다"* + 워크숍 끝나고 5분 도움
3. INSTALL.md "Common Troubleshooting" 섹션에 9가지 사례 정리되어 있음

### 시나리오 8 — 전체 전원/네트워크 실패 (최악)
**증상**: 강의실 정전·인터넷 완전 끊김·HarmonyOn 노트북도 다운
**즉시 대응**:
1. **인쇄된 페르소나 카드 30장** 학생들에게 무작위 4장씩 분배
2. 학생이 종이에 *"이 4명이 내 narratype에 어떻게 반응할까?"* 1인칭으로 작성 (5분)
3. AGENTS.md도 워크시트로 종이 작성 (인쇄 템플릿 사용)
4. Constellation은 화이트보드에 4사분면 (성장/붕괴/지속/변혁) 그려서 학생 작품 dot으로 표시
5. 종이 기반 워크숍도 충분히 의미 있음 — *"AI가 없어도 작동하는 디자인"* 자체가 spec design 메시지

---

## 진행자 협업 분담

| 시나리오 발생 시 | HarmonyOn 역할 | 교수님 역할 |
|---|---|---|
| 1 (HarmonyOn Ollama 실패) | 즉시 fallback 영상으로 전환, 30초 안에 정상화 시도 | 전체 진행 흐름 유지, 학생 짝꿍 활동 안내 |
| 2 (학생 폰 호환) | 페어링 안내 | 그룹 재배치 |
| 3 (시연 속도) | 모델 다운그레이드, 옵션 OFF | 진행 흐름 유지 |
| 4 (wifi) | 도구 단독 시연 + 학생 오프라인 토론 안내 | 진행 흐름 유지 |
| 5 (앱 크래시) | 즉시 복구 (15초) | 학생 짝꿍 review 시간 부여 |
| 6 (narratype 미준비) | [예시 로드] 시연 | 학생과 1:1 짧게 brainstorm |
| 7 (설치 시도 실패한 학생) | *"제 노트북 보세요"* 안내, 워크숍 후 도움 | 진행 흐름 유지 |
| 8 (전면 실패) | 종이 워크숍 자료 배포 | 종이 기반 진행 |

---

## 사전 점검 (워크숍 1시간 전)

- [ ] **HarmonyOn 노트북**: Ollama 켜져 있고 Gemma 4 E2B + E4B 로드 + Streamlit 한 라운드 정상 작동 확인
- [ ] 사전 녹화 데모 영상이 USB + 노트북 로컬에 있음 (Ollama 죽었을 때 즉시 재생)
- [ ] HarmonyOn 폰: Edge Gallery 작동 확인
- [ ] 강의실 wifi 속도 한 번 체크 (학생 cloud LLM 응답 5초 이내)
- [ ] 프로젝터·HDMI·USB 연결 확인 — 노트북 화면 미러링 OK
- [ ] 인쇄 자료 (페르소나 카드 30장 / narratype worksheet / AGENTS.md 예시 4개) 충분한 부수
- [ ] **30분 일찍 도착** → 설치 시도한 학생 트러블슈팅 + HarmonyOn ↔ 박은선 교수님 분담 확인

---

## 사후 (워크숍 후)

- [ ] 학생 피드백 짧은 설문 (옵션, 3-5문항)
- [ ] HarmonyOn 회고 메모 — 다음 워크숍 운영 시 참고
- [ ] 도구 GitHub repo 학생 피드백 반영 업데이트

---

Yonsei Speculative Design 2026 · BACKUP_PLAN.md
