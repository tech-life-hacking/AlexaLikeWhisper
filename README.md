# AlexaLikeWhisper
Implement of audio speech recognition "Whisper" released by OpenAI triggered on Wakeup word detection

The detail is [my articles](https://www.techlife-hacking.com/?p=1627).
# Demo
![AlexaLikeWhisper](https://www.techlife-hacking.com/wp-content/uploads/2022/10/whisper.gif)  
After detected wakeup words, whisper recognizes audio speech like Alexa!  
Using recognized words, you can control avatar robots or IoT...etc!  

# System
![System](https://www.techlife-hacking.com/wp-content/uploads/2022/10/whisper_en.png)  
Users : Say wakeup words like "Hey, Siri" and some speech  
PC : Input audio speech with a microphone and recognize it with whisper  
IoT : Using recognized words, do tasks  


# PC Spec
OS : Ubuntu 20.04  
GPU : Geforce RTX 2080Ti  
# Setup
## PC
### Install build dependencies
install pytorch  
Install Pytorch with matching GPU, CUDA and cuDNN versions.  
[Pytorch](https://www.techlife-hacking.com/?p=1325)  

```
# install transformers
pip install transformers

# install whisper
sudo apt update && sudo apt install ffmpeg
pip install git+https://github.com/openai/whisper.git

# install pyaudio
sudo apt-get install portaudio19-dev
pip install pyaudio

# install pvporcupine
pip install pvporcupine
```

To use pvporcupine, you need to register to [PICOVOICE](https://console.picovoice.ai/) and get a API Key.  
And download a model file(.ppn) and place it in AlexaLikeWhisper/model.  

# Usage
```
# get source of alexa like whisper and install alexa_like_whisper
git clone https://github.com/tech-life-hacking/AlexaLikeWhisper.git
cd AlexaLikeWhisper
pip install -e .
```
Place a model file(.ppn) in AlexaLikeWhisper/model.  

```python
import alexa_like_whisper

if __name__ == "__main__":
    # Modelsizes on whisper
    MODELSIZES = ['tiny', 'base', 'small', 'medium', 'large']

    # AccessKey obtained from Picovoice Console (https://console.picovoice.ai/)
    ACCESS_KEY = "YOUR_ACCESS_KEY"
    KEYWORD_PATH = ['PPN_FILE_PATH']

    # Recording Time(s)
    RECORDING_TIME = 3

    alexa_like = alexa_like_whisper.AlexaLikeWhisper(ACCESS_KEY, KEYWORD_PATH, MODELSIZES[3], RECORDING_TIME)

    while True:
        result = alexa_like.run()
        print(result)

```

result shows  
- Waiting wakeup words : "Sleep"
- After detected wakeup words and on recording : "On recording..."
- When recognizing audio speech : the result
