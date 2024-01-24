from utils.configreader import Config
from utils.logger import logger

config = Config("configs/config_1.json")

for tts, ttsobj in config.ttsDict.iteritems():
    logger.info(f"Creating the sound from {tts}")
    
print("complted")
 