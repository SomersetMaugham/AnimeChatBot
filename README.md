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
        ```
        ```bash
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
* **Ollama 모델 없음:** `ollama pull gemma3:latest` 명령 실행 여부 확인

## 참고 사이트

* Coding an Anime Chatbot: A Journey with LLaMA 3 [TTS + Anime Model]
* https://youtu.be/oCFm-rXI6HU?si=VHvYq3sUhe4rfh_j

* 2D Animation Character made by
*  B站@樱井檬
*  https://space.bilibili.com/4873028?spm_id_from=333.337.0.0
*  Twitter@sakurai_mon

## 라이선스
상업적인 사용은 금지합니다. 애니메이션 캐릭터의 저작권 및 모든 권리는 캐릭터 제작자에게 있습니다.
이하 내용은 캐릭터 제작자의 라이센스 문서를 번역한 것입니다.
----------------------------------------------------------------------------------------
이 모델은 MO.v1.3입니다.
사용 허가 안내
방송(라이브 스트리밍) 사용을 허용하며, 수익은 전부 사용자에게 귀속됩니다.
모델을 이용해 만든 외형으로 선물을 제작하여 증정하는 것은 허용되지만, 판매는 금지됩니다.
방송/영상 외의 상업적 행위는 금지됩니다.
(예: 회사나 그룹에 소속되어 데뷔하거나, 해당 모델로 플랫폼과 계약하는 것 등)

2차 배포 및 2차 판매는 금지됩니다.

소규모 텍스처 수정은 허용되나 문제 발생 시 보장되지 않습니다. 대규모 수정은 사전에 제작자에게 알릴 필요가 있습니다.

사용 안내

모델 제작자를 의도적으로 숨기는 행위는 금지됩니다.
이 모델은 여러 차례 테스트를 거쳐 문제가 없음을 확인하였습니다. 문제가 발생할 경우 먼저 자신의 페이셜 캡처 설정을 확인해 주세요.
본 모델은 음란물, 폭력, 정치 및 종교 관련 활동에 사용할 수 없습니다.
사용자가 법률 및 규정을 위반하거나 본 모델과 관련된 분쟁 및 논란을 일으킬 경우, 제작자는 책임지지 않으며 사용자 본인이 전적인 책임을 집니다.
일부 파츠 조합 시 클리핑(몸 뚫림) 현상이 발생할 수 있으며, 이는 정상입니다. 클리핑이 발생하지 않는 조합으로 사용을 권장합니다.

## 기여하기

기여는 언제나 환영입니다! 풀 리퀘스트나 이슈를 자유롭게 올려 주세요.
