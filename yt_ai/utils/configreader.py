import json
import importlib
import os
from yt_ai.utils.logger import logger
from yt_ai.utils.datareader import read_data_csv
from moviepy.config import change_settings


class Config:
    def __init__(self, configFile):
        self.configFile = configFile
        logger.info(f"Reading Config file from {configFile}")
        with open(self.configFile, "r") as f:
            self.config = json.load(f)
        
        os.environ['CURL_CA_BUNDLE'] = ''
        
        change_settings({"IMAGEMAGICK_BINARY": r"C:\Program Files\ImageMagick-7.1.1-Q16-HDRI\magick.exe"})
        
        logger.debug(f"Setting cache folder : {self.config['cache']}")
        os.environ['HF_DATASETS_CACHE']=self.config["cache"]
        if self.config["use_cpu"]:
            os.environ["CUDA_VISIBLE_DEVICES"] = ""
            os.environ["SUNO_OFFLOAD_CPU"] = "True"
            os.environ["SUNO_USE_SMALL_MODELS"] = "True"
        
        self.data = read_data_csv(self.config["dataFile"])

        # self._decode_tts()
        # self._decode_ttv()
        
    def decode_tts(self):
        ttsDict = {}
        for model in self.config["tts"]:
            logger.info(f"Loading tts model: {model}")
            # lazy loading
            module = importlib.import_module(f'yt_ai.tts.{model}')
            ttsDict[model] = getattr(module, f"{model}")(self.config)
            # self.ttsDict[model] = self.ttsDict[model]
        return ttsDict

    def decode_ttv(self):
        ttvDict = {}
        for model in self.config["ttv"]:
            logger.info(f"Loading ttv model: {model}")
             # lazy loading
            module = importlib.import_module(f'yt_ai.ttv.{model}')
            ttvDict[model] = getattr(module, f"{model}")(self.config)
        return ttvDict
            
  
    def get_config(self):
        return self.config

    def get_data(self):
        return self.data
