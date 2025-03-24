# Chat GPT in terminal but you can talk with it
 Chat GPT in console that can take audio input and uses tts to answer
<br />
few most important variables are in code to change if you want to
<br />
**PUT YOUR OPENAI API KEY IN _'api_key.txt'_ FILE**

# important commands:
Hold **CTRL + SHIFT + /** to talk or just write
<br />
**?history?** - shows the history of messages in current chat
<br />
**?reset?** or **CTRL + SHIFT + -** - resets the conversation - clears the history

<br />
<br />

Tested on windows 11 python 3.12 
<br />
To run you will need some libraries and I'm too lazy to do requirements.txt so im just gonna tell you here how to install everything you will need:
(those are the ones i used, newer or similar versions SHOULD work just fine)
<br>
<b>requirements:</b>
```
PyAudio==0.2.14
pydub==0.25.1
torch==2.3.0
keyboard==0.13.5
SpeechRecognition==3.10.4
requests==2.31.0
pyttsx3==2.90
gTTS==2.5.1
```
<br />
You will also need ffmpeg installed in system
you can do it like that:

```
winget install "FFmpeg (Essentials Build)"
```
Newer versions of all those libs should work just as fine

<br />
<br />

If you have any questions let me know :3
