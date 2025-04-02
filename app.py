import requests
from flask import Flask, render_template, request, jsonify
import sqlite3
from openai import OpenAI
import markdown2
import edge_tts
from io import BytesIO
from pydub import AudioSegment
import torch
from TTS.api import TTS
import os
import time
from TTS.tts.configs.xtts_config import XttsConfig  # Import XttsConfig
from TTS.tts.models.xtts import XttsAudioConfig # Import XttsAudioConfig
import re
import json
#import asyncio

app = Flask(__name__)

# System Prompt 설정
# system_prompt = "당신의 이름은 Aki입니다. 정확한 정보를, 예의바르게 한국어로만 대답해 주세요."

SETTINGS_FILE = "settings.json"

# vars
type_tts = 'edge'
#type_tts = 'coqui'
tts = None

# 설정 기본값
default_settings = {
    "llm": {
        "provider": "local", # Modify this line
        "model": "gemma3:latest", # Modify this line
        "apiKey": "",
        "serverIp": "127.0.0.1", # Add this line
        "serverPort": "11434" # Add this line
    },
    "tts": {
        "provider": "edge",
        "voice": "ko-KR-SunHiNeural",
        "speed": 120
    },
    "system": {
        "prompt": "당신의 이름은 MO입니다. 정확한 정보를, 예의바르게 한국어로만 대답해 주세요.",
        "language": "kr"
    }
}

# Load settings from settings.json
def load_settings():
    """Loads settings from the settings.json file."""
    try:
        with open(SETTINGS_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    except FileNotFoundError:
        print(f"Settings file not found. Using default settings.")
        return default_settings.copy()  # Return a copy to avoid modifying the default
    except json.JSONDecodeError:
        print(f"Error decoding settings file. Using default settings.")
        return default_settings.copy()

# Save settings to settings.json
def save_settings(settings):
    """Saves settings to the settings.json file."""
    with open(SETTINGS_FILE, "w", encoding="utf-8") as f:
        json.dump(settings, f, indent=4, ensure_ascii=False)


# 현재 설정값
current_settings = load_settings()


if type_tts == 'coqui':
    device = "cuda" if torch.cuda.is_available() else "cpu"

    # Add XttsConfig and XttsAudioConfig to safe globals
    torch.serialization.add_safe_globals([XttsConfig, XttsAudioConfig])  # Add both classes

    # Create a TTS instance to use list_models()
    # try:
    #     tts_instance = TTS(None)  # We pass None because we only want to list models
    # except Exception as e:
    #     print(f"Error creating TTS instance: {e}")
    #     exit()

    # # List available models using the instance
    # print("Available TTS models:")
    # available_models_manager = tts_instance.manager
    # available_models = available_models_manager.list_models()  # Corrected line
    # print(available_models)

    # # Find the correct model name from the list.
    # # It should be something like: "tts_models/multilingual/multi-dataset/xtts_v2"
    # # or "tts_models/multilingual/multi-dataset/your_model_name"
    # # Replace 'tts_models/multilingual/multi-dataset/xtts_v2' with the correct model identifier

    # # Find the correct model name from the list.
    # model_name = None
    # for model in available_models:
    #     if "xtts_v2" in model and "multilingual/multi-dataset" in model:
    #         model_name = model
    #         break

    # if model_name is None:
    #     print("Error: xtts_v2 model not found in available models.")
    #     exit()

    # print(f"Using model: {model_name}")

    # try:
    #     tts = TTS(model_name).to(device)
    # except Exception as e:
    #     print(f"Error loading model {model_name}: {e}")
    #     exit()

# ... (rest of your code - no changes needed below this line) ...
# Connect to the database (SQLITE)
conn = sqlite3.connect('messages.db', check_same_thread=False)
c = conn.cursor()

# Create a table if it doesn't exist
c.execute('''CREATE TABLE IF NOT EXISTS messages
             (role TEXT,
              content TEXT)''')

# c.execute('''ALTER TABLE chat_messages RENAME TO messages''')

# Commit the changes and close the connection
conn.commit()

# Voice assistant

# Clear text
def remove_emojis_and_pattern(text):
    """
    Removes emojis, specific patterns, and HTML tags from a given text.
    Args:
        text: The input string.
    Returns:
        The cleaned string.
    """
    # Remove emojis (more specific pattern)
    emoji_pattern = re.compile("["
                               u"\U0001F600-\U0001F64F"  # emoticons
                               u"\U0001F300-\U0001F5FF"  # symbols & pictographs
                               u"\U0001F680-\U0001F6FF"  # transport & map symbols
                               u"\U0001F1E0-\U0001F1FF"  # flags (iOS)
                               u"\U0001F900-\U0001F9FF"  # Supplemental Symbols and Pictographs
                               u"\U0001FA70-\U0001FAFF"  # Symbols and Pictographs Extended-A
                               u"\U0001F300-\U0001F5FF"  # Miscellaneous Symbols and Pictographs
                               u"\U0001F600-\U0001F64F"  # Emoticons
                               u"\U0001F680-\U0001F6FF"  # Transport and Map Symbols
                               u"\U0001F700-\U0001F77F"  # Alchemical Symbols
                               u"\U0001F780-\U0001F7FF"  # Geometric Shapes Extended
                               u"\U0001F800-\U0001F8FF"  # Supplemental Arrows-C
                               u"\U0001F900-\U0001F9FF"  # Supplemental Symbols and Pictographs
                               u"\U0001FA00-\U0001FA6F"  # Chess Symbols
                               u"\U0001FA70-\U0001FAFF"  # Symbols and Pictographs Extended-A
                               u"\U0001FB00-\U0001FBFF"  # Symbols and Pictographs Extended-B
                               u"\u2600-\u26FF"  # Miscellaneous Symbols
                               u"\u2700-\u27BF"  # Dingbats
                               u"\u2B00-\u2BFF"  # Miscellaneous Symbols and Arrows
                               u"\u2300-\u23FF"  # Miscellaneous Technical
                               u"\u25A0-\u25FF"  # Geometric Shapes
                               u"\u200d"
                               u"\u23cf"
                               u"\u23e9"
                               u"\u231a"
                               u"\ufe0f"  # dingbats
                               u"\u3030"
                               "]+", flags=re.UNICODE)
    text = emoji_pattern.sub(r'', text)

    # Remove specific patterns
    text = text.replace('~', '').replace('_', '')
    text = re.sub(r'\*\[.*?\]\*', '', text)
    text = text.replace('*', '').replace('=', '').replace('#', '')

    # Remove <em> tags (HTML)
    text = re.sub(r'<em>((.|\n)*?)</em>', '', text)
    # Remove &lt;em&gt; tags (HTML encoded)
    text = re.sub(r'&lt;em&gt;((.|\n)*?)&lt;/em&gt;', '', text)
    # Remove content within parentheses (including the parentheses)
    text = re.sub(r'\(.*?\)', '', text)

    return text

# Edge
async def synth_audio_edge(TEXT, temp_file, voice, speed) -> None:
    """
    Synthesizes audio using the Edge TTS engine.

    Args:
        TEXT: The text to synthesize.
        temp_file: The path to save the temporary audio file.
        voice: The voice to use for synthesis.
        speed: The speed percentage (e.g., 120 for 120%).
    """
    # speed_percentage를 edge_tts에서 사용하는 rate 형식으로 변환
    if speed > 100:
        rate = f"+{speed - 100}%"
    elif speed < 100:
        rate = f"-{100 - speed}%"
    else:
        rate = "+0%"
    
    print(f"synth_audio_edge voice: {voice}, rate: {rate}")
        
    communicate = edge_tts.Communicate(TEXT, voice, rate=rate)
    byte_array = bytearray()
    try:
        async for chunk in communicate.stream():
            if chunk["type"] == "audio":
                byte_array.extend(chunk["data"])
        audio_data = BytesIO(byte_array)
        audio_segment = AudioSegment.from_file(audio_data)
        audio_segment.export(temp_file, format="wav")
    except Exception as e:
        print(f"Error: {e}")
        return None
    return temp_file

async def call_generate(text, temp_file, tts=None):
    if type_tts == "edge":
        # Use settings from current_settings if tts_settings is not provided
        voice = current_settings["tts"]["voice"]
        speed = current_settings["tts"]["speed"]
        print(f"voice: {voice}, speed: {speed}")
        # if tts_settings is None:
        #     voice = current_settings["tts"]["voice"]
        #     speed = current_settings["tts"]["speed"]
        #     print(f"voice: {voice}, speed: {speed}")
        # else:
        #     voice = tts_settings["voice"]
        #     speed = tts_settings["speed"]
        #     print(f"voice: {voice}, speed: {speed}")
        await synth_audio_edge(text, temp_file, voice, speed)
    elif type_tts == "coqui":
        # coqui
        if tts is None:
            # 모델 로딩 (Lazy Loading)
            model_name = "tts_models/multilingual/multi-dataset/xtts_v2" # 모델명 직접 지정
            try:
                tts = TTS(model_name).to(device)
            except Exception as e:
                print(f"Error loading model {model_name}: {e}")
                exit()
        tts.tts_to_file(text=text, file_path=temp_file)
    return temp_file

async def synthesize(text, filename):
    text = remove_emojis_and_pattern(text)
    
    print("[Before synth After remv]"+text)
    # clear ./static/audio/ folder
    for file in os.listdir("./static/audio/"):
        os.remove("./static/audio/" + file)

    timestamp = time.strftime("%Y%m%d-%H%M%S")
    temp_file = f"./static/audio/{filename}_{timestamp}.wav"

    path_out = await call_generate(text, temp_file, tts=tts)
    #path_out = await call_generate(text, temp_file)
    # TODO:RVC
    final_file = f"./static/audio/output.wav"

    return path_out

system_prompt = current_settings["system"]["prompt"]

def getAnswer(role, text):
    # Insert the message into the database
    c.execute("INSERT INTO messages VALUES (?, ?)", (role, text))
    conn.commit()

    # Get the last 5 messages
    c.execute("SELECT * FROM messages ORDER BY rowid DESC LIMIT 5")
    previous_messages = [{"role": row[0], "content": row[1]} for row in c.fetchall()]

    # REVERSE
    previous_messages = list(reversed(previous_messages))

    # Add the system prompt
    if "system" not in [x["role"] for x in previous_messages]:
        previous_messages = [{"role": "system", "content": system_prompt}] + previous_messages

    # 현재 설정에서 LLM 정보 가져오기
    llm_provider = current_settings["llm"]["provider"]
    llm_model = current_settings["llm"]["model"]
    
    # 기본값은 Ollama 사용
    base_url = "http://192.168.219.100:11434/v1"
    api_key = "ollama"
    model = "gemma3:latest"
    
    # 설정에 따라 API 정보 변경
    if llm_provider == "local":
        base_url = "http://"+current_settings["llm"]["serverIp"]+":"+current_settings["llm"]["serverPort"]+"/v1" # Modify this line
        api_key = "ollama"
        model = llm_model
    elif llm_provider == "openai" or llm_provider == "chatgpt":
        base_url = "https://api.openai.com/v1"
        api_key = current_settings["llm"]["apiKey"]
        model = llm_model
    elif llm_provider == "anthropic":
        base_url = "https://api.anthropic.com/v1"
        api_key = current_settings["llm"]["apiKey"]
        model = llm_model
    elif llm_provider == "deepseek":
        base_url = "https://api.deepseek.com/v1"
        api_key = current_settings["llm"]["apiKey"]
        model = llm_model
    elif llm_provider == "gemini":
        base_url = "https://generativelanguage.googleapis.com/v1"
        api_key = current_settings["llm"]["apiKey"]
        model = llm_model
    
    client = OpenAI(base_url=base_url, api_key=api_key)
    response = client.chat.completions.create(
        model=model,
        messages=previous_messages,
        temperature=0.7,
    )

    print("Base URL:"+base_url)
    print("API Key:"+api_key)
    print("Model:"+model)
 
    bot_response = response.choices[0].message.content.strip()

    c.execute("INSERT INTO messages VALUES (?, ?)", ("assistant", bot_response))
    conn.commit()

    return bot_response

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/settings')
def settings():
    return render_template('settings.html')

@app.route('/echo', methods=['POST'])
def echo():
    data = request.json
    message = data['message']
    return jsonify({'FROM': 'Echobot', 'MESSAGE': message})


@app.route('/chat', methods=['POST'])
async def chat():
    data = request.json
    message = getAnswer("user", data['message'])

    # Run the async function in a separate thread
    # loop = asyncio.new_event_loop()
    # asyncio.set_event_loop(loop)
    # return jsonify({'FROM': 'Aki', 'MESSAGE': markdown2.markdown(message)})
    name_wav = await synthesize(message, "out")
    return jsonify({'FROM': 'MO', 'MESSAGE': markdown2.markdown(message), 'WAV': name_wav})


# history
@app.route('/history', methods=['GET'])
def history():
    c.execute("SELECT * FROM messages ORDER BY rowid DESC LIMIT 5")
    previous_messages = [{"role": row[0], "content": markdown2.markdown(row[1])} for row in c.fetchall()]
    return jsonify(previous_messages)


# 설정 관련 API 엔드포인트
@app.route('/update_settings', methods=['POST'])
def update_settings():
    global current_settings, system_prompt
    print("update_settings function called!")  # Debugging message 1    
    try:
        new_settings = request.json
        
        print("Received new_settings:", new_settings)  # Debugging message 2
        
        print("Current settings before update:", current_settings) # Debugging message 3

        current_settings = new_settings

        print("Current settings after update:", current_settings) # Debugging message 4        
        
        # 시스템 프롬프트 업데이트
        system_prompt = current_settings["system"]["prompt"]

        print("system_prompt after update:", system_prompt) # Debugging message 5

        # Save the updated settings to the file
        save_settings(current_settings)

        return jsonify({"success": True, "message": "설정이 업데이트되었습니다."})
    except Exception as e:

        print(f"Error updating settings: {str(e)}")  # Debugging message 6
        
        return jsonify({"success": False, "message": f"설정 업데이트 중 오류가 발생했습니다: {str(e)}"})


@app.route('/get_settings', methods=['GET'])
def get_settings():
    global current_settings
    print("get_settings function called!")
    current_settings = load_settings()
    
    return jsonify(current_settings)


@app.route('/test_voice', methods=['POST'])
async def test_voice():
    try:
        data = request.json
        text = data.get('text', '안녕하세요, 음성 테스트입니다.')
        
        tts_settings = {
            "provider": data.get('provider', 'edge'),
            "voice": data.get('voice', 'en-IE-EmilyNeural'),
            "speed": data.get('speed', 110)
        }
        
        timestamp = time.strftime("%Y%m%d-%H%M%S")
        temp_file = f"./static/audio/test_{timestamp}.wav"
        
        audio_path = await call_generate(text, temp_file, tts_settings)
        
        return jsonify({"success": True, "audio_url": audio_path})
    except Exception as e:
        return jsonify({"success": False, "message": f"음성 테스트 중 오류가 발생했습니다: {str(e)}"})


@app.route('/clear_history', methods=['POST'])
def clear_history():
    try:
        c.execute("DELETE FROM messages")
        conn.commit()
        return jsonify({"success": True, "message": "대화 기록이 삭제되었습니다."})
    except Exception as e:
        return jsonify({"success": False, "message": f"대화 기록 삭제 중 오류가 발생했습니다: {str(e)}"})

@app.route('/get_ollama_models', methods=['POST'])
def get_ollama_models():
    """
    Fetches the list of available models from a remote Ollama server.
    """
    try:
        data = request.json
        server_ip = data.get('serverIp')
        server_port = data.get('serverPort')
        
        if not server_ip or not server_port:
            return jsonify({"success": False, "message": "Server IP and Port are required."}), 400

        base_url = f"http://{server_ip}:{server_port}/api/tags"
        print("base_url:"+base_url)
        response = requests.get(base_url)
        response.raise_for_status()  # Raise an exception for bad status codes

        models_data = response.json()
        models = [model["name"] for model in models_data["models"]]
        print("models:"+str(models))

        return jsonify({"success": True, "models": models})

    except requests.exceptions.RequestException as e:
        print(f"Error connecting to Ollama server: {e}")
        return jsonify({"success": False, "message": f"Error connecting to Ollama server: {e}"}), 500
    except Exception as e:
        print(f"Error fetching Ollama models: {e}")
        return jsonify({"success": False, "message": f"Error fetching Ollama models: {e}"}), 500    
    
if __name__ == '__main__':
    app.run(debug=True)
