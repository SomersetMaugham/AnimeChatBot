# MO: A Cute Anime Girl Chatbot

MO is a fun and interactive chatbot designed to simulate a conversation with a cute anime girl. This project utilizes a combination of technologies, including OpenAI's language models, edge-tts or coqui-tts for voice synthesis, and a Flask-based web interface.

## Features

*   **Interactive Chat:** Engage in dynamic conversations with MO.
*   **Anime Girl Persona:** MO embodies the personality of a cute anime girl, complete with playful teasing.
*   **Voice Synthesis:** Hear MO's responses through voice synthesis (either Edge TTS or Coqui TTS).
*   **Markdown Support:** Responses are formatted using Markdown for enhanced readability.
*   **Conversation History:** The chatbot remembers recent interactions, providing context for ongoing conversations.
*   **Customizable:** Easily modify MO's personality and behavior by changing the system prompt.
* **Local LLM:** Use local LLM(ollama)

## Technologies Used

*   **Flask:** Web framework for the chatbot's interface.
*   **OpenAI API:** (or Local LLM) Powers the chatbot's language understanding and response generation.
*   **Edge TTS:** (Optional) Microsoft's text-to-speech service for voice synthesis.
*   **Coqui TTS:** (Optional) An alternative open-source text-to-speech engine.
*   **SQLite:** Database for storing conversation history.
*   **Markdown2:** For rendering Markdown in the chatbot's responses.
*   **Python:** The primary programming language.
* **Ollama:** Local LLM

## Installation

### Prerequisites

*   **Python 3.8+:** Make sure you have Python 3.8 or a later version installed.
*   **pip:** Python's package installer.
*   **Ollama:** Local LLM. [https://ollama.com/](https://ollama.com/)

### Setting up a Virtual Environment (Recommended)

Using a virtual environment is highly recommended to avoid conflicts with other Python projects. Here are two popular methods:

#### 1. Using `conda`

1.  **Install conda:** If you don't have conda, download and install it from https://www.anaconda.com/.
2.  **Create a new environment:**
    ```bash
    conda create --name aki-chatbot python=3.10
    ```
    (Replace `aki-chatbot` with your desired environment name and `3.10` with your preferred Python version.)
3.  **Activate the environment:**
    ```bash
    conda activate aki-chatbot
    ```

#### 2. Using `pyenv` and `venv`

1.  **Install pyenv:** Follow the instructions for your operating system from https://github.com/pyenv/pyenv.
2.  **Install a Python version:**
    ```bash
    pyenv install 3.10.13
    ```
    (Replace `3.10.13` with your preferred Python version.)
3.  **Create a virtual environment:**
    ```bash
    python3 -m venv .venv
    ```
4.  **Activate the environment:**
    ```bash
    source .venv/bin/activate  # On Linux/macOS
    .venv\Scripts\activate  # On Windows
    ```

### Installing Dependencies

1.  **Clone the repository:**
    ```bash
    git clone <YOUR_REPOSITORY_URL>
    cd <YOUR_REPOSITORY_DIRECTORY>
    ```
    (Replace `<YOUR_REPOSITORY_URL>` with your GitHub repository URL and `<YOUR_REPOSITORY_DIRECTORY>` with the directory name.)
2.  **Install the required packages:**
    ```bash
    pip install -r requirements.txt
    ```
3.  **Install the pytorch packages:**
    For Windows without GPU and MacOS:
    ```bash
    pip install torch torchvision torchaudio 
   
    ```
    For Windows with GPU:
    ```bash
    pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu118
    ```

### Configuration

1.  **Ollama:**
    *   Install Ollama from https://ollama.com/
    *   Run `ollama serve` in your terminal.
    *   Run `ollama pull gemma3` in your terminal.
2.  **TTS Engine:**
    *   **Edge TTS (Default):** No additional setup is required.
    *   **Coqui TTS:**
        *   Install `TTS` with `pip install TTS`.
        *   The code will automatically download the `xtts_v2` model if it's not already present.
        *   If you want to use a different model, modify the `type_tts` variable in `app.py` and `reserved.py` to `coqui` and change the model name in the code.
3. **voice file:**
    * If you want to use coqui-tts, you need to create a `voice` folder and put the `voice.wav` file in it.

## Usage

1.  **Activate the virtual environment:** (If you created one)
    ```bash
    conda activate aki-chatbot  # If using conda
    source .venv/bin/activate  # If using pyenv/venv (Linux/macOS)
    .venv\Scripts\activate  # If using pyenv/venv (Windows)
    ```
2.  **Run the Flask application:**
    ```bash
    python app.py
    ```
3.  **Access the chatbot:** Open your web browser and go to `http://127.0.0.1:5000/`.
4. **Chat:** Start chatting with Aki!

## Customization

*   **System Prompt:** Modify the `system_prompt` variable in `app.py` to change Aki's personality and behavior.
*   **TTS Engine:** Switch between Edge TTS and Coqui TTS by changing the `type_tts` variable in `app.py` and `reserved.py`.
*   **Model:** If you use coqui-tts, you can change the model name in `app.py` and `reserved.py`.

## Troubleshooting

*   **Error loading model:** If you encounter an error loading the Coqui TTS model, ensure that you have a stable internet connection and that the model name is correct.
*   **Ollama not running:** Make sure you have run `ollama serve` in your terminal.
* **Ollama model not found:** Make sure you have run `ollama pull gemma3` in your terminal.

## Contributing

Contributions are welcome! Please feel free to submit pull requests or open issues.
