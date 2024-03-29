from bark import  generate_audio, preload_models
from scipy.io.wavfile import write as write_wav
import numpy as np
from pathlib import Path
from yt_ai.utils.logger import logger
import pytorch_seed

class BarkTTS:
    def __init__(self, config_file):
        self.config_file = config_file
        self.output = Path(config_file["outPath"])/__name__.split(".")[-1]
        self.output.mkdir(exist_ok=True,parents=True)
        self.sample_rate = int(self.config_file["tts"]["BarkTTS"]["talking_speed"] * 22050)
        # download and load all models
        preload_models()
        self.audio_array = np.zeros((1,), dtype=np.float32)

    def create_audio(self, text_prompt, interval = 1):
        empty_ = np.zeros((interval*self.sample_rate,), dtype=np.float32)
        # generate audio from text
        # TODO: set seed as user input
        with pytorch_seed.SavedRNG(123):
            array_data = generate_audio(text_prompt,  history_prompt=self.config_file["tts"]["BarkTTS"]["speaker"])
            self.audio_array = np.hstack((self.audio_array, empty_, array_data))
    
    def save_audio(self, file_name):
        # save audio to disk
        write_wav(self.output / file_name, self.sample_rate, self.audio_array)
        logger.info(f"Saved audio for {self.output / file_name}")
        
    def get_audio(self):
        return self.audio_array
