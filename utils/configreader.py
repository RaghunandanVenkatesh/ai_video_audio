import json
import importlib
import os
from utils.logger import logger

class Config:
    def __init__(self, configFile):
        self.configFile = configFile
        with open(self.configFile, "r") as f:
            self.config = json.load(f)
            
        os.environ['HF_DATASETS_CACHE']=self.config["cache"]
        self.ttsDict = {}
        self.ttvDict = {}
        self._decode_tts()
        self._decode_ttv()
        
    def _decode_tts(self):
        for model in self.config["tts"]:
            logger.info(f"Loading tts model: {model}")
            # lazy loading
            module = importlib.import_module(f'tts.{model}')
            self.ttsDict[model] = getattr(module, f"{model}")(self.config)
            # self.ttsDict[model] = self.ttsDict[model]

    def _decode_ttv(self):
         for model in self.config["ttv"]:
            logger.info(f"Loading ttv model: {model}")
             
             # lazy loading
            module = importlib.import_module(f'ttv.{model}')
            self.ttvDict[model] = getattr(module, f"{model}")(self.config)
            
    def get_tts_dict(self):
        return self.ttsDict
    
    def get_ttv_dict(self):
        return self.ttvDict
    