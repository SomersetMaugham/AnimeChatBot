
# Aki: 귀여운 애니메이션 소녀 챗봇

Aki는 귀엽고 장난기 많은 애니메이션 소녀와 대화하는 듯한 경험을 제공하는 재미있는 인터랙티브 챗봇입니다. 사용자를 살짝 놀리기도 하며, 독특한 개성을 통해 대화에 생동감을 더합니다. 이 프로젝트는 OpenAI 언어 모델, edge-tts 또는 coqui-tts 음성 합성 기술, Flask 기반 웹 인터페이스 등을 조합하여 구현되었습니다.

## 주요 기능

* **인터랙티브 채팅:** Aki와 동적인 대화를 나눌 수 있습니다.
* **애니메 소녀 페르소나:** 귀엽고 장난기 많은 애니메 캐릭터로서의 Aki.
* **음성 합성:** Aki의 응답을 음성으로 들을 수 있습니다 (Edge TTS 또는 Coqui TTS 사용).
* **마크다운 지원:** 응답은 마크다운 형식으로 보기 쉽게 출력됩니다.
* **대화 기록 유지:** 최근 대화를 기억하여 자연스러운 이어말하기가 가능합니다.
* **사용자 맞춤화:** `system prompt`를 수정하여 Aki의 성격과 행동을 쉽게 바꿀 수 있습니다.
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
    conda create --name aki-chatbot python=3.10
    ```
3. 환경 활성화:
    ```bash
    conda activate aki-chatbot
    ```

#### 2. `pyenv`와 `venv` 사용 시

1. `pyenv` 설치: https://github.com/pyenv/pyenv
2. Python 버전 설치:
    ```bash
    pyenv install 3.10.13
    ```
3. 가상 환경 생성:
    ```bash
    python3 -m venv .venv
    ```
4. 가상 환경 활성화:
    ```bash
    source .venv/bin/activate  # (Linux/macOS)
    .venv\Scriptsctivate  # (Windows)
    ```

### 의존성 설치

1. Git 저장소 클론:
    ```bash
    git clone <YOUR_REPOSITORY_URL>
    cd <YOUR_REPOSITORY_DIRECTORY>
    ```
2. 패키지 설치:
    ```bash
    pip install -r requirements.txt
    ```
3. PyTorch 설치:
    - GPU 없이 (Windows) 또는 macOS:
    ```bash
    pip install torch torchvision torchaudio
    ```
    - GPU 사용 시 (Windows):
    ```bash
    pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu118
    ```

### 설정

1. **Ollama:**
    * https://ollama.com/에서 Ollama 설치
    * 터미널에서 다음 실행:
        ```bash
        ollama serve
        ollama pull gemma3
        ```

2. **TTS 엔진:**
    * **Edge TTS (기본):** 별도 설정 없음.
    * **Coqui TTS 사용 시:**
        * `pip install TTS`로 설치
        * `xtts_v2` 모델이 없으면 자동 다운로드
        * 다른 모델 사용 시, `app.py`와 `reserved.py`에서 `type_tts`를 `coqui`로 변경하고 모델 이름도 수정

3. **음성 파일:**
    * Coqui-tts를 사용할 경우, `voice` 폴더를 만들고 `voice.wav` 파일을 넣어야 합니다.

## 사용 방법

1. 가상 환경 활성화:
    ```bash
    conda activate aki-chatbot  # conda 사용 시
    source .venv/bin/activate  # Linux/macOS
    .venv\Scriptsctivate  # Windows
    ```
2. Flask 앱 실행:
    ```bash
    python app.py
    ```
3. 웹 브라우저에서 접속: `http://127.0.0.1:5000/`
4. Aki와 대화 시작!

## 사용자 정의

* `app.py`의 `system_prompt`를 수정해 Aki의 성격과 말투 변경 가능
* `app.py` 및 `reserved.py`의 `type_tts`로 음성 합성 엔진 전환 가능
* Coqui TTS 모델 이름도 위 파일에서 수정 가능

## 문제 해결

* **모델 로딩 오류:** 인터넷 연결 상태와 모델 이름 확인
* **Ollama 실행되지 않음:** `ollama serve` 명령 실행 여부 확인
* **Ollama 모델 없음:** `ollama pull gemma3` 명령 실행 여부 확인

## 라이선스

MIT 라이선스를 따릅니다. 자세한 사항은 LICENSE 파일을 참고하세요.

## 기여하기

기여는 언제나 환영입니다! 풀 리퀘스트나 이슈를 자유롭게 올려 주세요.
