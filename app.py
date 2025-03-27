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
#import asyncio

# vars
type_tts = 'edge'
#type_tts = 'coqui'
tts = None

if type_tts == 'coqui':
    device = "cuda" if torch.cuda.is_available() else "cpu"

    # Add XttsConfig and XttsAudioConfig to safe globals
    torch.serialization.add_safe_globals([XttsConfig, XttsAudioConfig])  # Add both classes

    # Create a TTS instance to use list_models()
    try:
        tts_instance = TTS(None)  # We pass None because we only want to list models
    except Exception as e:
        print(f"Error creating TTS instance: {e}")
        exit()

    # List available models using the instance
    print("Available TTS models:")
    available_models_manager = tts_instance.manager
    available_models = available_models_manager.list_models()  # Corrected line
    print(available_models)

    # Find the correct model name from the list.
    # It should be something like: "tts_models/multilingual/multi-dataset/xtts_v2"
    # or "tts_models/multilingual/multi-dataset/your_model_name"
    # Replace 'tts_models/multilingual/multi-dataset/xtts_v2' with the correct model identifier

    # Find the correct model name from the list.
    model_name = None
    for model in available_models:
        if "xtts_v2" in model and "multilingual/multi-dataset" in model:
            model_name = model
            break

    if model_name is None:
        print("Error: xtts_v2 model not found in available models.")
        exit()

    print(f"Using model: {model_name}")

    try:
        tts = TTS(model_name).to(device)
    except Exception as e:
        print(f"Error loading model {model_name}: {e}")
        exit()

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
    # Remove emojis
    emoji_pattern = re.compile("["
                               u"\U0001F600-\U0001F64F"  # emoticons
                               u"\U0001F300-\U0001F5FF"  # symbols & pictographs
                               u"\U0001F680-\U0001F6FF"  # transport & map symbols
                               u"\U0001F1E0-\U0001F1FF"  # flags (iOS)
                               u"\U00002500-\U00002BEF"  # chinese char
                               u"\U00002702-\U000027B0"
                               u"\U00002702-\U000027B0"
                               u"\U000024C2-\U0001F251"
                               u"\U0001f926-\U0001f937"
                               u"\U00010000-\U0010ffff"
                               u"\u2640-\u2642"
                               u"\u2600-\u2B55"
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
async def synth_audio_edge(TEXT, temp_file) -> None:
    VOICE = "en-IE-EmilyNeural"
    communicate = edge_tts.Communicate(TEXT, VOICE, rate="+10%")
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
#async def call_generate(text, temp_file):
    if type_tts == "edge":
        await synth_audio_edge(text, temp_file)
    else:
        # coqui
        #tts.tts_to_file(text=text, speaker_wav="voice/voice.wav", language="en", file_path=temp_file)
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


system_prompt = "You are named Aki. Pretend you're my cute anime assistant. Please respond simple and politely. Do NOT USE INTERJECTION!"

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

    client = OpenAI(base_url="http://localhost:11434/v1", api_key="ollama")
    response = client.chat.completions.create(
        model="gemma3:latest:",
        messages=previous_messages,
        temperature=0.7,
    )

    bot_response = response.choices[0].message.content.strip()

    c.execute("INSERT INTO messages VALUES (?, ?)", ("assistant", bot_response))
    conn.commit()

    return bot_response


app = Flask(__name__)


@app.route('/')
def index():
    return render_template('index.html')


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
    return jsonify({'FROM': 'Aki', 'MESSAGE': markdown2.markdown(message), 'WAV': name_wav})


# history
@app.route('/history', methods=['GET'])
def history():
    c.execute("SELECT * FROM messages ORDER BY rowid DESC LIMIT 5")
    previous_messages = [{"role": row[0], "content": markdown2.markdown(row[1])} for row in c.fetchall()]
    return jsonify(previous_messages)


if __name__ == '__main__':
    app.run(debug=True)
