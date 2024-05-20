import speech_recognition as sr
from pydub import AudioSegment
from pydub.playback import play
import pyaudio
import wave
import keyboard
import requests
import pyttsx3
from gtts import gTTS
import subprocess
import threading

######### important variables ###########

model = 'gpt-3.5-turbo' #gpt model
temperature = 1 #keep within 0 - 1 higher values can cause crashing
voice = 0 #if you have one langueage in windows keep this at 0 or maybe it will work at 1 if you have more you can try higher numbers

#########################################
with open("api_key.txt", "r") as f:
    api_key = f.read()

messages = []

print("program started...")
transcribed = ""

r = sr.Recognizer()
audio = pyaudio.PyAudio()
engine = pyttsx3.init() 

start = AudioSegment.from_wav("sound_effects/start_listening.wav")
end = AudioSegment.from_wav("sound_effects/end_listening.wav")

FORMAT = pyaudio.paInt16  # Audio format
CHANNELS = 1  # Number of channels
RATE = 44100  # Sampling rate
CHUNK = 1024  # Chunk size

def userMessageAdder(text):
    messages.append({'role': 'user', 'content': text})
def systemMessageAdder(text):
    messages.append({'role': 'system', 'content': text})
def gpt(text):
    headers = {
    'Content-Type': 'application/json',
    'Authorization': 'Bearer ' + api_key,
    }

    json_data = {
        'model': model,
        'messages':
            messages
        ,
        'temperature': temperature,
    }
    response = requests.post('https://api.openai.com/v1/chat/completions', headers=headers, json=json_data)
    return response.json()['choices'][0]['message']['content']
def start_recording():
    play(start)
    global stream, frames
    stream = audio.open(format=FORMAT, channels=CHANNELS, rate=RATE, input=True, frames_per_buffer=CHUNK)
    frames = []
    print("")
    print("Recording started...")
def stop_recording():
    global stream, frames
    stream.stop_stream()
    stream.close()
    print("Recording stopped...")

    wf = wave.open("output.wav", 'wb')
    wf.setnchannels(CHANNELS)
    wf.setsampwidth(audio.get_sample_size(FORMAT))
    wf.setframerate(RATE)
    wf.writeframes(b''.join(frames))
    wf.close()
    print("Recording saved as output.wav")
    play(end)
def textInput(text):
    if text == "?history?":
        print(messages)
    elif text == "?reset?":
        messages.clear()
        print("message history cleared")
    else:
        userMessageAdder(text)
        gpted = gpt(text)
        systemMessageAdder(gpted)
        print(gpted)
        print("waiting for next command...")

def input_thread():
    global user_input
    while True:
        user_input = input("")
        if user_input:
            textInput(user_input)
def main():
    global stream, frames

    threading.Thread(target=input_thread, daemon=True).start()

    while True:
        if keyboard.is_pressed('ctrl+shift+-'):
            messages.clear()
            print("message history cleared")

        if keyboard.is_pressed('ctrl+shift+/'):
            if stream is None or not stream.is_active():
                start_recording()
        
        if stream is not None and stream.is_active():
            data = stream.read(CHUNK)
            frames.append(data)
        
        if not keyboard.is_pressed('ctrl+shift+/') and stream is not None and stream.is_active():
            stop_recording()
            print("")
            recocnize_audio("output.wav")
            break
def recocnize_audio(audio):
    r = sr.Recognizer()
    with sr.AudioFile(audio) as source:
        recording = r.record(source)
    try:
        transcribed = r.recognize_google(recording)
        print(transcribed)
        print("")
        userMessageAdder(transcribed)
        gpted = gpt(transcribed)
        systemMessageAdder(gpted)
        print(gpted)
        # ttsGoogle(gpted)
        ttsBuildIn(gpted)
        print("waiting for next command...")
    except sr.UnknownValueError:
        print("Google Speech Recognition could not understand audio")
    except sr.RequestError as e:
        print("Could not request results from Google Speech Recognition service; {0}".format(e))

def ttsGoogle(text):
    tts = gTTS(text, lang='en', tld='us')
    tts.save('rec.mp3')
    play_mp3('rec.mp3')
    print("finished playing")

def ttsBuildIn(text):
    voices = engine.getProperty('voices')
    engine.setProperty('voice', voices[voice].id)
    engine.say(text)
    engine.runAndWait()

def play_mp3(file_path):
    ffmpeg_command = [
        'ffmpeg',
        '-i', file_path,     # Input file
        '-f', 's16le',       # Output format: signed 16-bit little-endian
        '-acodec', 'pcm_s16le',  # Audio codec
        '-ar', '44100',      # Sampling rate
        '-ac', '2',          # Number of channels
        '-'                  # Output to stdout
    ]

    process = subprocess.Popen(ffmpeg_command, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

    p = pyaudio.PyAudio()
    stream = p.open(format=pyaudio.paInt16, channels=2, rate=44100, output=True)

    chunk_size = 1024
    while True:
        data = process.stdout.read(chunk_size)
        if not data:
            break
        stream.write(data)

    stream.stop_stream()
    stream.close()
    p.terminate()

    process.stdout.close()
    process.stderr.close()
    process.wait()

while True:
    if __name__ == "__main__":
        stream = None
        frames = []
        main()

#on device speech to text #high quality
# try:
#     print(r.recognize_whisper(audio))
# except sr.UnknownValueError:
#     print("Whisper could not understand audio")
# except sr.RequestError as e:
#     print(f"Could not request results from Whisper; {e}")