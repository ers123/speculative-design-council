# Installation Guide / 설치 가이드

> **Speculative Design Council** — local AI tool for 2026 Yonsei SD workshop.
> This guide is bilingual: Korean section first, English section below.
>
> 이 가이드는 이중 언어입니다: 한국어 먼저, 영어는 아래쪽.

---

## Choose your section / 섹션 선택

- [한국어 가이드](#한국어-가이드) — 한국어 사용자
- [English Guide](#english-guide) — for non-Korean speakers
- [Common Troubleshooting / 공통 문제 해결](#common-troubleshooting--공통-문제-해결)

---

# 한국어 가이드

## 0. 시작 전 — 컴퓨터 사양 확인

| 항목 | 최소 | 권장 |
|---|---|---|
| OS | macOS 11+ / Windows 10+ | macOS 13+ / Windows 11 |
| RAM | 8GB | 16GB+ |
| 디스크 여유 공간 | 10GB | 20GB+ |
| 인터넷 | 첫 설치 시 필요 (~3-5GB 다운로드) | 설치 후 오프라인 작동 가능 |

> 사양이 부족하면 4-5명 1조에 강한 노트북 1대로 페어링 권장.

---

## 1. Ollama 설치 (로컬 AI 엔진)

### Mac

**A. Homebrew 사용 (권장)**

터미널 열기 (Spotlight → "Terminal"):
```bash
brew install ollama
```

Homebrew가 없다면 먼저 설치:
```bash
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
```

**B. 공식 인스톨러 사용**
https://ollama.com 접속 → "Download for macOS" 클릭 → .dmg 다운로드 → 설치 (드래그)

### Windows

1. https://ollama.com/download 접속
2. "Download for Windows" 클릭 → `OllamaSetup.exe` 다운로드
3. 인스톨러 실행 (관리자 권한 필요할 수 있음)
4. 설치 완료 후 자동으로 백그라운드 서비스로 실행됨

### 설치 확인

터미널 (Windows: PowerShell 또는 명령 프롬프트, Mac: Terminal)에서:
```bash
ollama --version
```
버전이 보이면 성공.

---

## 2. Gemma 4 모델 다운로드 (2개)

워크숍 표준 구성 — 가벼운 모델 1개 + 약간 더 좋은 모델 1개:

```bash
# E2B — 가벼움, 1.5GB RAM, 빠름 (default 권장)
ollama pull gemma4:e2b

# E4B — 더 깊은 추론, 약간 큼 (~2GB RAM)
ollama pull gemma4:e4b
```

다운로드 시간: 두 개 합쳐 약 10-20분 (네트워크 속도에 따라). Wi-Fi 환경 권장.

(선택) 더 빠른 응답을 원하면 MTP 가속 모델 추가:
```bash
ollama pull gemma4-mtp
```

> 본 워크숍은 더 큰 모델 (deepseek-r1, qwen3.5 등)을 **요구하지 않습니다**. E2B + E4B만으로 충분.

설치된 모델 확인:
```bash
ollama list
```

기대 출력: `gemma4:e2b ~1.5GB, gemma4:e4b ~2GB` 두 줄 이상.

---

## 3. Python 3 설치

### Mac

대부분의 최신 Mac에는 이미 설치되어 있음. 확인:
```bash
python3 --version
```
`Python 3.10` 이상이면 OK. 없으면:
```bash
brew install python@3.11
```

### Windows

1. https://www.python.org/downloads/ 접속
2. "Download Python 3.11.x" 클릭
3. 인스톨러 실행 — **반드시 "Add Python to PATH" 체크박스 선택!**
4. "Install Now" 클릭

설치 확인 (새 PowerShell 창에서):
```bash
python --version
```
또는
```bash
py --version
```

---

## 4. Council 코드 다운로드

### 옵션 A: GitHub (Git 사용)

```bash
git clone https://github.com/[강사가 알려주는 URL]/streamlit_spec_design_council.git
cd streamlit_spec_design_council
```

### 옵션 B: ZIP 다운로드 (Git 없을 때)

1. 강사가 제공한 zip 파일 다운로드
2. 압축 해제 → 폴더 안으로 이동:
   - Mac: Finder에서 폴더 열기 → 우클릭 → "Open in Terminal" (또는 터미널에서 `cd` 로 이동)
   - Windows: 폴더 열기 → 주소창에 `cmd` 입력 → Enter

---

## 5. Python 가상환경 + 의존성 설치

폴더 안에서 (즉 `streamlit_spec_design_council/` 디렉토리에 있는 상태):

### Mac

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt
```

> Mac에서 `pip install ...` 가 실패하고 "externally-managed-environment" 에러:  
> `python -m pip install ...` 을 사용하세요 (위 명령처럼).

### Windows

```bash
python -m venv .venv
.venv\Scripts\activate
python -m pip install -r requirements.txt
```

> Windows에서 PowerShell이 venv 활성화 스크립트 실행을 막으면:  
> `Set-ExecutionPolicy -Scope CurrentUser -ExecutionPolicy RemoteSigned` 한 번 실행 후 다시 시도.

설치 시간: 2-5분. streamlit, ollama, python-docx, pypdf, openpyxl 등 자동 설치.

---

## 6. 실행

같은 폴더, venv 활성화된 상태에서:

```bash
streamlit run app.py
```

브라우저가 자동으로 열림 (http://localhost:8501).

종료: 터미널에서 `Ctrl + C` (Mac에서도 Cmd가 아니라 Control).

다음 번에 다시 실행할 때:
```bash
cd streamlit_spec_design_council
# Mac:
source .venv/bin/activate
# Windows:
.venv\Scripts\activate

streamlit run app.py
```

---

## 7. 사용 흐름 (앱 안에서)

1. **사이드바 최상단**: 언어 선택 (한국어 / English)
2. **사이드바 모델**: 자동으로 가장 작은 모델 선택됨 (default = gemma4)
3. **(선택) 사이드바 Council 구성**: `Nemotron-Personas-Korea 샘플 30명.xlsx` 업로드 → [AI 추천 Council 구성] 클릭
4. **메인 영역 프로젝트**: 드롭다운에서 예시 narratype 선택하고 [예시 로드] 또는 본인 narratype 직접 입력
5. **메인 영역 단계**: "Narratype 분석" 선택 (첫 단계 권장) — 단계 설명 박스가 자동으로 보임
6. **[Council 실행]** 클릭 → 거울 → 지도 → 의장 순서로 자동 진행
7. 결과 확인 후 하단에서 .docx / AGENTS.md / Constellation 좌표 다운로드

---

# English Guide

## 0. Before You Start — Hardware Check

| Item | Minimum | Recommended |
|---|---|---|
| OS | macOS 11+ / Windows 10+ | macOS 13+ / Windows 11 |
| RAM | 8GB | 16GB+ |
| Free disk space | 10GB | 20GB+ |
| Internet | Required for initial install (~3-5GB download) | Works offline after install |

> If your laptop is below spec, pair up: 1 capable laptop per 4-5 students.

---

## 1. Install Ollama (Local AI Engine)

### Mac

**A. Using Homebrew (recommended)**

Open Terminal (Spotlight → "Terminal"):
```bash
brew install ollama
```

If Homebrew isn't installed yet:
```bash
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
```

**B. Official installer**

Visit https://ollama.com → "Download for macOS" → drag the .dmg.

### Windows

1. Go to https://ollama.com/download
2. Click "Download for Windows" → `OllamaSetup.exe`
3. Run the installer (may require admin rights)
4. After install, Ollama runs as a background service automatically.

### Verify

In terminal (Windows: PowerShell or Command Prompt; Mac: Terminal):
```bash
ollama --version
```
Version number = success.

---

## 2. Download Gemma 4 Models (2 of them)

Workshop standard setup — one lighter model + one slightly heavier:

```bash
# E2B — light, 1.5GB RAM, fast (recommended default)
ollama pull gemma4:e2b

# E4B — deeper reasoning, slightly bigger (~2GB RAM)
ollama pull gemma4:e4b
```

Download time: ~10-20 min for both combined. Use Wi-Fi.

(Optional) For faster responses, also pull the MTP drafter:
```bash
ollama pull gemma4-mtp
```

> The workshop does NOT require heavier models (deepseek-r1, qwen3.5, etc.). E2B + E4B is enough.

Verify:
```bash
ollama list
```

Expected: at least `gemma4:e2b ~1.5GB` and `gemma4:e4b ~2GB`.

---

## 3. Install Python 3

### Mac

Most modern Macs already have Python. Check:
```bash
python3 --version
```
If you see `Python 3.10` or higher, you're good. Otherwise:
```bash
brew install python@3.11
```

### Windows

1. Visit https://www.python.org/downloads/
2. Click "Download Python 3.11.x"
3. Run installer — **YOU MUST CHECK "Add Python to PATH" CHECKBOX!**
4. Click "Install Now".

Verify (in a new PowerShell window):
```bash
python --version
```
Or:
```bash
py --version
```

---

## 4. Download the Council Code

### Option A: GitHub (with Git)

```bash
git clone https://github.com/[instructor will share URL]/streamlit_spec_design_council.git
cd streamlit_spec_design_council
```

### Option B: ZIP download (no Git)

1. Download zip provided by your instructor.
2. Unzip and navigate into the folder:
   - Mac: Open folder in Finder → right-click → "Open in Terminal" (or `cd` from Terminal).
   - Windows: Open folder → type `cmd` in the address bar → press Enter.

---

## 5. Python Virtual Environment + Dependencies

Inside the folder (so you're in `streamlit_spec_design_council/`):

### Mac

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt
```

> If `pip install ...` fails with "externally-managed-environment":  
> use `python -m pip install ...` instead (as shown above).

### Windows

```bash
python -m venv .venv
.venv\Scripts\activate
python -m pip install -r requirements.txt
```

> If PowerShell blocks the venv activation script:  
> run `Set-ExecutionPolicy -Scope CurrentUser -ExecutionPolicy RemoteSigned` once, then retry.

Install time: 2-5 minutes. Installs streamlit, ollama, python-docx, pypdf, openpyxl, etc.

---

## 6. Run

In the same folder, with venv activated:

```bash
streamlit run app.py
```

Your browser will open automatically (http://localhost:8501).

To quit: in the terminal, press `Ctrl + C` (use Control on Mac too, not Command).

To run again later:
```bash
cd streamlit_spec_design_council
# Mac:
source .venv/bin/activate
# Windows:
.venv\Scripts\activate

streamlit run app.py
```

---

## 7. Usage Flow (inside the app)

1. **Sidebar top**: pick your language (한국어 / English)
2. **Sidebar model**: smallest model auto-selected (default = gemma4)
3. **(Optional) Sidebar Council Composition**: upload `Nemotron-Personas-Korea 샘플 30명.xlsx` → click [AI-Recommend Council]
4. **Main area Project**: choose an example narratype from dropdown and [Load example], OR write your own narratype
5. **Main area Stage**: pick "Narratype 분석" (recommended first stage) — a description box auto-appears
6. Click **[Run Council]** → Mirror → Map → Chairman run sequentially
7. After results, scroll down to download .docx / AGENTS.md / Constellation coordinates

---

# Common Troubleshooting / 공통 문제 해결

## Issue 1: `ollama: command not found` / `ollama: 명령을 찾을 수 없음`

**원인 / Cause**: Ollama installed but not in PATH.

**해결 / Fix**:
- Mac: Close and reopen Terminal. If still failing: `brew install ollama` again.
- Windows: Restart computer once. PATH gets refreshed at boot.

---

## Issue 2: `Could not connect to ollama server` (앱에서 빨간색 표시)

**원인 / Cause**: Ollama service not running.

**해결 / Fix**:
- Mac: `ollama serve` (run in a separate terminal window, leave it open)
- Windows: Open Task Manager → check if "Ollama" is running. If not, restart computer once.

---

## Issue 3: `externally-managed-environment` (pip install 시 Mac)

**원인 / Cause**: Homebrew Python PEP 668 protection.

**해결 / Fix**: Always use `python -m pip install ...` (not bare `pip install`).

Alternative: if `python -m pip` also fails, you may have a shell alias overriding pip. Try:
```bash
\pip install -r requirements.txt
# or
unalias pip && pip install -r requirements.txt
```

---

## Issue 4: PowerShell 활성화 스크립트 차단 / PowerShell blocks activation script (Windows)

**원인 / Cause**: PowerShell execution policy restricts unsigned scripts.

**해결 / Fix**: Run **once** in PowerShell (as admin if needed):
```bash
Set-ExecutionPolicy -Scope CurrentUser -ExecutionPolicy RemoteSigned
```
Then retry `.venv\Scripts\activate`.

---

## Issue 5: Council 실행 후 응답이 매우 느림 / Council Run is very slow

**원인 / Cause**:
- 첫 호출 = 모델 메모리 로딩 5-10초
- 큰 모델 (deepseek-r1:14b 등) 사용 중
- RAM 부족 → 디스크 swap

**해결 / Fix**:
- 가장 작은 모델 (gemma4) 사용 — 사이드바 모델 영역 default
- 사고 모드 (thinking) 끄기 — 사이드바 토글
- 다른 무거운 앱 종료
- N라운드 설정 1로 (default)

---

## Issue 6: 출력에 ``` 같은 코드 펜스가 보임 / Output contains stray ``` fences

**원인 / Cause**: LLM occasionally wraps markdown in code fences despite instructions.

**해결 / Fix**: 자동으로 사후 제거됨. 그래도 보이면 같은 단계 [해당 단계만 재실행] 클릭.

---

## Issue 7: 메모리 부족 / Out of memory

**증상**: app crashes mid-Council run, or extremely slow.

**해결 / Fix**:
- Switch to smaller model: sidebar → top model option
- Close other RAM-heavy apps (Chrome with many tabs, Slack, etc.)
- Disable thinking mode
- If still failing: pair with a classmate who has a stronger laptop.

---

## Issue 8: 한국어 글자가 깨져서 보임 / Korean characters appear as boxes

**원인 / Cause**: Browser/OS missing Korean font.

**해결 / Fix**:
- Mac: 보통 기본 설치됨. System Preferences → Language & Region → Add Korean.
- Windows: Settings → Time & Language → Language → Add Korean language pack.
- Or use a different browser (Chrome/Edge/Safari/Firefox).

---

## Issue 9: GitHub에서 코드를 받을 수 없음 / Cannot clone from GitHub

**해결 / Fix**: Use Option B (ZIP download) — your instructor will provide a direct link.

---

## Getting Help / 도움 받기

If stuck:
1. Take a screenshot of the error.
2. Note your OS + version + which step failed.
3. Ask in class group chat or contact instructor/workshop facilitator.

학기 중 도움이 필요하면:
1. 에러 화면 스크린샷
2. OS + 버전 + 어느 단계에서 실패했는지 메모
3. 수업 단톡방 또는 강사/워크숍 진행자에게 문의

---

## 참고 / Reference

- **Ollama docs**: https://ollama.com/docs
- **Gemma 4 model card**: https://huggingface.co/google/gemma-4-E2B
- **Streamlit docs**: https://docs.streamlit.io
- **Council source code**: in this folder (README.md, agents.py, app.py)

Generated for Yonsei Speculative Design 2026 workshop · 2026.05.11
