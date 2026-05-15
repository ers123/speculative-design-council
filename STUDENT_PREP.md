# 워크숍 사전 준비 안내 / Workshop Pre-announcement

> Yonsei University Speculative Design 2026 · AI Trigger Workshop
>
> **15분이면 끝나는 준비입니다.** 노트북에 복잡한 설치는 필요 없습니다.
> Only ~15 min of prep needed. No complex laptop installation required.

---

### 꼭 해와야 할 것 3가지 — 워크숍 1주 전까지

#### ① 스마트폰: 앱 하나 설치 (5분)
- **앱 이름**: Google AI Edge Gallery
- **다운로드**: [App Store](https://apps.apple.com/us/app/google-ai-edge-gallery/id6749645337) 또는 Google Play에서 *"Google AI Edge Gallery"* 검색
- **앱 열기 → "Gemma 4 E2B" 모델 다운로드** (약 1.5GB, Wi-Fi 환경 권장, 선택: 가능하면 E4B도 다운) 
- 다 받아지면 *"안녕하세요"* 한 번 보내서 응답 받으면 끝
- iOS 17 미만 또는 구형 Android는 호환 안 될 수 있음 → 워크숍 당일 옆 친구 폰 같이 보세요 (괜찮습니다)
- 그래도 본인 기기로 직접 해보고 싶다면 아래 **①-B Plan B** 참조

#### ①-B 폰 설치가 안 될 때 — Plan B (선택)

폰이 호환 안 되면 **노트북에 Ollama + Gemma 4 E2B**를 설치해서 *"거울 (Mirror)"* 역할을 대신할 수 있습니다. 어떤 노트북에서도 무조건 작동하는 안전망입니다 (Mac/Windows/Linux, RAM 4GB+).

```bash
# Mac
brew install ollama
ollama pull gemma4:e2b
ollama run gemma4:e2b "안녕"
```

Windows·상세 설치는 [council/INSTALL.md](council/INSTALL.md)의 **1번·2번 단계만** 따라하시면 됩니다 (5-10분, Streamlit 전체 설치 X).

워크숍 당일 폰 대신 터미널에서 `ollama run gemma4:e2b`로 "거울" AI와 대화하세요. 인터넷 끊겨도 작동합니다.

#### ② 본인이 평소 쓰는 AI 한 번 켜보기 (2분)
ChatGPT / Claude / Gemini / Perplexity 중 **본인이 평소 쓰던 것** 그대로. **새로 가입할 필요 없습니다**. 워크숍 당일 브라우저 탭에 하나 열어두기.

#### ③ 본인 narratype 200자 작성 (10분)
자세한 가이드: [NARRATYPE_WORKSHEET.md](NARRATYPE_WORKSHEET.md) 참조 (한·영)

간단히:
- **장소·시점** (예: "2045년 서울")
- **트리거 기술** (예: "안면 감정 분석")
- **인물** (예: "30대 직장인")
- **비판하는 현재 사회의 element**
- 위 4개를 묶어 200-400자 한 단락으로

2025년 학생 작품 4개를 워크시트에서 예시로 볼 수 있습니다.

---

### 워크숍에서 어떻게 쓰이나

| 도구 | 어디서 | 워크숍 안 역할 |
|---|---|---|
| Edge Gallery (폰) | 본인 스마트폰 | **"거울 (Mirror)"** — 작고 사적인 AI |
| ChatGPT 등 (브라우저) | 본인 노트북 브라우저 | **"지도 (Map)"** — 크고 공적인 AI |
| narratype 200자 메모 | 핸드폰 메모장 / 노트 | 본인 작업 시작점 |

워크숍 핵심 활동: 폰의 AI와 브라우저의 AI 사이를 본인이 직접 오가며 *"본인 narratype을 어떻게 다르게 다루는가"* 체험.

---

### 💡 도전해보고 싶다면 (완전 선택사항)

**위 3가지만 해와도 워크숍 참여 충분합니다.** 더 깊이 해보고 싶은 학생이라면 노트북에 **Streamlit Council 도구**를 미리 설치해 올 수도 있어요. 수업 시간에 직접 시연하니, 걱정하지 마세요.

설치 가이드 (한·영, Mac+Windows): **[INSTALL.md](council/INSTALL.md)**

설치 어렵거나 시간 부족하면 **건너뛰셔도 됩니다**. 워크숍 당일 시연으로 충분히 봅니다.

설치 실패해도 부담 갖지 마세요. 수업 당일에 도와드리겠습니다.

---

### 사전 체크리스트 (워크숍 전날)

- [ ] 폰에서 Edge Gallery 열고 Gemma 4 E2B로 *"안녕"* 한 줄 응답 받음 (또는 Plan B: 노트북 `ollama run gemma4:e2b` 응답 확인)
- [ ] 평소 쓰는 cloud AI 로그인 확인
- [ ] narratype 200자 메모장·노트에 작성 완료
- [ ] (선택) 노트북 Streamlit Council 설치 시도

---

## English Guide

### 3 Required Items — 1 week before workshop

#### ① Phone: install one app (5 min)
- **App name**: Google AI Edge Gallery
- **Download**: [App Store](https://apps.apple.com/us/app/google-ai-edge-gallery/id6749645337) or Google Play (search *"Google AI Edge Gallery"*)
- **Open app → download "Gemma 4 E2B" model** (~1.5GB, Wi-Fi recommended, Optional: download "Gemma 4 E4B")
- When ready, send *"hello"* — get a response. Done.
- iOS<17 or older Android may not be compatible → pair with classmate on workshop day, totally fine
- Want to run it on your own device anyway? See **①-B Plan B** below

#### ①-B If phone install fails — Plan B (optional)

If your phone is incompatible, install **Ollama + Gemma 4 E2B on your laptop** to play the *"Mirror"* role instead. This works on any laptop (Mac/Windows/Linux, RAM 4GB+) — a universal safety net.

```bash
# Mac
brew install ollama
ollama pull gemma4:e2b
ollama run gemma4:e2b "hello"
```

Windows · full guide: follow **steps 1 and 2 only** of [council/INSTALL.md](council/INSTALL.md) (5-10 min, you don't need the full Streamlit install).

On workshop day, use terminal `ollama run gemma4:e2b` as your "Mirror" AI instead of the phone. Works offline.

#### ② Open the cloud AI you usually use (2 min)
ChatGPT / Claude / Gemini / Perplexity — **whichever you already use**. **No new signup needed**. Just have it open in a browser tab on workshop day.

#### ③ Write your narratype (200 chars, ~10 min)
Detailed guide: [NARRATYPE_WORKSHEET.md](NARRATYPE_WORKSHEET.md) (bilingual)

Quick version:
- **Place & time** (e.g. "Seoul 2045")
- **Triggering technology** (e.g. "facial emotion analysis")
- **Characters** (e.g. "30s office worker")
- **What aspect of current society are you critiquing?**
- Combine into one paragraph, 200-400 chars

The worksheet has 4 examples from 2025 students.

---

### How they're used in the workshop

| Tool | Where | Role in workshop |
|---|---|---|
| Edge Gallery (phone) | Your smartphone | **"Mirror"** — small, private AI |
| ChatGPT etc. (browser) | Your laptop browser | **"Map"** — large, public AI |
| Narratype 200 chars | Phone notepad / notebook | Your work's starting point |

Core workshop activity: move back and forth manually between phone AI and browser AI, experience *"how they treat your narratype differently."*

---

### 💡 If you want to go deeper (completely optional)

**The 3 items above are enough for full workshop participation.** If you want to go deeper, you can pre-install the **Streamlit Council tool** on your laptop. The lecturer will demo it in the workshop, so you can follow along without installing.

Installation guide (bilingual, Mac+Win): **[INSTALL.md](council/INSTALL.md)**

If installation is hard or you don't have time, **skip it**. The workshop demo will be enough.

If you tried but failed, no worries.

---

### Pre-flight checklist (day before)

- [ ] Phone: Edge Gallery responds to *"hello"* with Gemma 4 E2B (or Plan B: laptop `ollama run gemma4:e2b` responds)
- [ ] Cloud AI logged in
- [ ] Narratype 200 chars written
- [ ] (Optional) Tried Streamlit Council install

---

Yonsei Speculative Design 2026 · STUDENT_PREP.md
