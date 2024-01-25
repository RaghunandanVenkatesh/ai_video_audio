from bark import SAMPLE_RATE, generate_audio, preload_models
from scipy.io.wavfile import write as write_wav
import os
from pathlib import Path
os.environ['CURL_CA_BUNDLE'] = ''


class BarkTTS:
    def __init__(self, config_file):
        self.config_file = config_file
        self.output = Path(config_file["outPath"])/__name__
        # download and load all models
        preload_models()
        self.audio_array = []

    def create_audio(self, text_prompt):
        # generate audio from text
        self.audio_array = generate_audio(text_prompt)
    
    def save_audio(self, file_name):
        # save audio to disk
        write_wav(self.output / file_name, SAMPLE_RATE, self.audio_array)
        
    def get_audio(self):
        return self.audio_array
        # play text in notebook
        # Audio(audio_array, rate=SAMPLE_RATE)