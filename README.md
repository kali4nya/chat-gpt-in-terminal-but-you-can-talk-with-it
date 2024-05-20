# Chat GPT in terminal but you can talk with him
 Chat GPT in console that can take audio input and uses tts to answer

few most important variables are in code to change if you want to

**PUT YOUR OPENAI API KEY IN _'api_key.txt'_ file**

# important commands:
**?history?** - shows the history of messages in current chat
**?reset?** - resets the conversation - clears the history



tested on windows 11 python 3.12
to run you will need some libraries and I'm too lazy to do requirements.txt so im just gonna tell you here how to install everything you will need:
```
pip install PyAudio==0.2.14
```
```
pip install pydub==0.25.1
```
```
pip install torch==2.3.0
```
```
pip install keyboard==0.13.5
```
```
pip install SpeechRecognition==3.10.4
```
```
pip install requests==2.31.0
```
```
pip install pyttsx3==2.90
```
```
pip install gTTS==2.5.1
```
you also need ffmpeg installed in system
you can do it like that:
```
winget install "FFmpeg (Essentials Build)"
```
