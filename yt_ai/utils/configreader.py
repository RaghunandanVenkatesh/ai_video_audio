import json
import importlib #This module provides a way to import modules programmatically.
import os
from yt_ai.utils.logger import logger #A custom logger imported from yt_ai.utils.logger that is used for logging information, warnings, and errors.
from yt_ai.utils.datareader import read_data_csv
from moviepy.config import change_settings #This is a function from the moviepy library, used to change settings such as the path to ImageMagick.

class Config:    #This defines the Config class, which will encapsulate the logic for loading and handling the configuration settings.
    def __init__(self, configFile):
        self.configFile = configFile   #This is the path to the JSON configuration file.
        logger.info(f"Reading Config file from {configFile}")   #The constructor logs that it is reading the configuration file.
        with open(self.configFile, "r") as f:
            self.config = json.load(f)   #The JSON file is opened and loaded into a dictionary, which is stored in self.config
        
        os.environ['CURL_CA_BUNDLE'] = '' #This sets the environment variable CURL_CA_BUNDLE to an empty string, which is necessary for certain operations in moviepy that involve image processing and likely to disable SSL verification (though this might have security implications).
        
        change_settings({"IMAGEMAGICK_BINARY": r"C:\Program Files\ImageMagick-7.1.1-Q16-HDRI\magick.exe"})  #This sets the path to the ImageMagick binary, which is necessary for certain operations in moviepy that involve image process.
        
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
