# GitHub 푸시 가이드 (본인용)

> 본 폴더(`streamlit_spec_design_council/`)를 https://github.com/ers123 계정에 새 repo로 푸시하는 step-by-step.

---

## 사전 점검

본인 Mac에서:

```bash
# Git 설치 확인
git --version
# 없으면: brew install git

# GitHub 계정 로그인 확인 (gh CLI 사용 시)
gh auth status
# 없으면: brew install gh && gh auth login
```

GitHub.com 웹사이트에서 `ers123` 계정으로 로그인.

---

## Step 1 — GitHub에서 빈 repo 만들기 (웹)

1. https://github.com/new 접속
2. 입력:
   - **Repository name**: `speculative-design-council` (또는 `sd-council`)
   - **Description**: `Local AI tool for Yonsei 2026 Speculative Design class — 4-agent Council with Ollama + Gemma 4`
   - **Public** 선택 (학생들이 clone 받기 위함)
   - **Add a README file** 체크 ❌ 안 함 (이미 있음)
   - **Add .gitignore** ❌ 안 함 (이미 있음)
   - **Add a license** ❌ 안 함 (이미 있음)
3. **Create repository** 클릭

생성 후 URL: `https://github.com/ers123/speculative-design-council`

---

## Step 2 — 로컬 폴더에서 git 초기화 + 푸시

터미널에서:

```bash
cd ~/Downloads/work/Yonsei/SD_2026_05/streamlit_spec_design_council

# venv·sessions·캐시 제거 안 함 (.gitignore가 알아서 제외)
# 단, 혹시 모를 잔여 정리:
rm -rf __pycache__ .sessions

# Git 초기화
git init -b main

# 모든 파일 추가
git add .

# .gitignore 동작 확인 (다음 항목들이 안 나와야 함):
#   .venv/, .sessions/, __pycache__/
git status
```

기대 출력:
```
On branch main
No commits yet
Changes to be committed:
  new file:   .gitignore
  new file:   CONVERSION.md
  new file:   DEMO_SCRIPT_SD.md
  new file:   INSTALL.md
  new file:   LICENSE
  new file:   PUSH_TO_GITHUB.md
  new file:   README.md
  new file:   agents.py
  new file:   app.py
  new file:   class_constellation.py
  new file:   e2e_test.py
  new file:   exporters.py
  new file:   personas.py
  new file:   requirements.txt
  new file:   resources.py
  new file:   sessions.py
  new file:   smoke_test.py
  new file:   templates.py
```

`.venv/`, `.sessions/`, `__pycache__/` 가 보이면 멈추고 `.gitignore` 확인.

이어서:

```bash
# 첫 커밋
git commit -m "Initial release v1.0 — Speculative Design Council for Yonsei 2026 SD class

Features:
- 4-agent Council (Mirror/Map/Chairman/Futurist) over Ollama + Gemma 4
- 3 stages: narratype analysis / AGENTS.md authoring / audience reaction
- Persona Council (Nemotron-Personas-Korea integration)
- N-round iteration (1-5 rounds)
- Bilingual UI (한국어 / English)
- Class-wide Constellation visualization tool
- Bilingual installation guide (Mac + Windows)
- Forked from streamlit_research_team (HarmonyOn)"

# 원격 저장소 연결
git remote add origin https://github.com/ers123/speculative-design-council.git

# 푸시
git push -u origin main
```

GitHub 계정 인증 요청 시:
- **Username**: `ers123`
- **Password**: GitHub Personal Access Token (PAT — 일반 비밀번호 아님)
- PAT 발급: https://github.com/settings/tokens → "Generate new token (classic)" → repo 권한 체크

또는 `gh auth login` 사용 (간편):
```bash
brew install gh
gh auth login
# 브라우저로 로그인 → 토큰 자동 저장
# 이후 git push 시 자동 인증
```

---

## Step 3 — 학생 배포 안내 (Repo URL 공유)

```
https://github.com/ers123/speculative-design-council
```

학생들에게:
```
1. 위 URL 접속
2. 초록색 [Code] 버튼 → "Download ZIP" 클릭 (Git 모르면)
3. 또는 터미널에서: git clone https://github.com/ers123/speculative-design-council.git
4. 설치는 INSTALL.md 참조
```

---

## Step 4 — 추후 업데이트 푸시

워크숍 후 코드 수정·버그 패치 했을 때:

```bash
cd ~/Downloads/work/Yonsei/SD_2026_05/streamlit_spec_design_council
git add .
git commit -m "fix: [무엇을 고쳤는지 한 줄]"
git push
```

---

## Step 5 — 학생 contributing 받기 (선택)

학생이 PR 보낼 수 있게 하려면 — README.md 하단에 추가:
```markdown
## Contributing

Pull requests welcome from Yonsei 2026 SD class students.
Workshop facilitator may merge contributions after review.
```

---

## 트러블슈팅

### `git push` 실패: "Authentication failed"
→ PAT 만료됐거나 잘못된 비밀번호. https://github.com/settings/tokens 에서 새 토큰 발급.

### `git push` 실패: "Updates were rejected"
→ GitHub repo가 비어있지 않음. README나 LICENSE 자동 추가했으면 충돌. 해결:
```bash
git pull --rebase origin main
git push
```

### Repo 크기가 큼 경고
→ persona Excel 파일들 (`Nemotron-Personas-Korea 샘플 *.xlsx`)이 streamlit_spec_design_council/ 안에 있지 않을 것. 외부 `SD_2026_05/` 폴더에 있어 자동 제외됨. 만약 폴더 안에 복사돼 있으면 .gitignore에 `*.xlsx` 추가 고려.

### Demo HTML 파일 (`class_constellation_demo.html`) 푸시할까?
→ 결정 사항. 푸시하면 학생이 데모 보기 쉬움. 안 푸시하면 `class_constellation.py --demo`로 학생이 직접 생성 필요. 현재 폴더에는 있는데 .gitignore 에 명시 안 됨 — 그대로 푸시될 것.

---

## 최종 확인

푸시 후 https://github.com/ers123/speculative-design-council 에서:
- [ ] README.md 메인에 보이는지
- [ ] INSTALL.md 클릭 시 양국어 가이드 정상 렌더링
- [ ] LICENSE 인식되는지 (우측 사이드바에 Apache-2.0 표시)
- [ ] requirements.txt 의 모든 dependency 명시
- [ ] `.venv/` 가 push 안 됐는지 (✅)
