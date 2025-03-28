English version: [README_en.md](README_en.md)

# MO: 귀여운 애니메이션 챗봇

애니메이션 소녀와 대화하는 듯한 경험을 제공하는 재미있는 인터랙티브 챗봇입니다. 이 프로젝트는 Gemma 언어 모델, edge-tts(또는 coqui-tts) 음성 합성 기술, Flask 기반 웹 인터페이스 등을 조합하여 구현되었습니다.

## 주요 기능

* **인터랙티브 채팅:** MO와 동적인 대화를 나눌 수 있습니다.
* **음성 합성:** MO의 응답을 음성으로 들을 수 있습니다 (Edge TTS 사용).
* **마크다운 지원:** 응답은 마크다운 형식으로 보기 쉽게 출력됩니다.
* **대화 기록 유지:** 최근 대화를 기억하여 자연스러운 이어말하기가 가능합니다.
* **사용자 맞춤화:** `system prompt`를 수정하여 MO의 성격과 행동을 쉽게 바꿀 수 있습니다.
* **로컬 LLM 지원:** Ollama를 통해 로컬 LLM을 사용할 수 있습니다.

## 사용 기술

* **Flask:** 챗봇 인터페이스를 위한 웹 프레임워크.
* **OpenAI API:** (또는 로컬 LLM) 챗봇의 언어 이해 및 응답 생성 기능을 담당.
* **Edge TTS:** (선택 사항) Microsoft의 텍스트-음성 변환 서비스.
* **Coqui TTS:** (선택 사항) 오픈소스 텍스트-음성 변환 엔진.
* **SQLite:** 대화 기록 저장용 데이터베이스.
* **Markdown2:** 챗봇 응답을 마크다운으로 렌더링.
* **Python:** 주요 프로그래밍 언어.
* **Ollama:** 로컬 LLM 플랫폼.

## 설치 방법

### 사전 준비 사항

* **Python 3.8 이상**  
* **pip** (Python 패키지 설치 관리자)  
* **Ollama** (https://ollama.com/)

### 가상 환경 설정 (권장)

다른 Python 프로젝트와의 충돌을 방지하기 위해 가상 환경 사용을 권장합니다.

#### 1. `conda` 사용 시

1. [https://www.anaconda.com/](https://www.anaconda.com/)에서 conda 설치
2. 새 환경 생성:
    ```bash
    conda create -n chatbot python=3.11
    ```
3. 환경 활성화:
    ```bash
    conda activate chatbot
    ```

### 의존성 설치

1. Git 저장소 클론:
    ```bash
    git clone https://github.com/SomersetMaugham/AnimeChatBot.git
    ```
    ```bash
    cd animechatbot
    ```
2. 패키지 설치:
    ```bash
    pip install -r requirements.txt
    ```
3. PyTorch 설치:
    - Nvidia GPU가 없을 때
    ```bash
    pip install torch torchvision torchaudio
    ```
    - Nvidia GPU가 있을 때
    ```bash
    pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu118
    ```

### 설정

1. **Ollama:**
    * [ollama](https://ollama.com) 에서 Ollama 설치
    * 터미널에서 다음 실행:
        ```bash
        ollama serve
        ollama pull gemma3:latest
        ```
2. **TTS 엔진:**
    * **Edge TTS (기본):** 별도 설정 없음.

3. **음성 파일:**
    * Coqui-tts를 사용할 경우, `voice` 폴더를 만들고 `voice.wav` 파일을 넣어야 합니다.

## 사용 방법

1. 가상 환경 활성화:
    ```bash
    conda activate chatbot  # conda 사용 시
    ```
2. Flask 앱 실행:
    ```bash
    python app.py
    ```
3. 웹 브라우저에서 접속: `http://127.0.0.1:5000/`
4. MO와 대화 시작!

## 사용자 정의

* `app.py`의 `system_prompt`를 수정해 MO의 성격과 말투 변경 가능

## 문제 해결

* **모델 로딩 오류:** 인터넷 연결 상태와 모델 이름 확인
* **Ollama 실행되지 않음:** `ollama serve` 명령 실행 여부 확인
* **Ollama 모델 없음:** `ollama pull gemma3` 명령 실행 여부 확인

## 참고 사이트

* Coding an Anime Chatbot: A Journey with LLaMA 3 [TTS + Anime Model]
* https://youtu.be/oCFm-rXI6HU?si=VHvYq3sUhe4rfh_j

## 라이선스

MIT 라이선스를 따릅니다. 자세한 사항은 LICENSE 파일을 참고하세요.

## 기여하기

기여는 언제나 환영입니다! 풀 리퀘스트나 이슈를 자유롭게 올려 주세요.
