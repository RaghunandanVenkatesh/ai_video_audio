from yt_ai.utils.configreader import Config
from yt_ai.utils.logger import logger

class Core:
    def __init__(self, config_file):
        self.config = Config(config_file)
        self.ttsDict = self.config.decode_tts()
        self.ttvDict = self.config.decode_ttv()
        
    def run(self):
        # iterate over the data file
        for id, id_df in self.config.get_data().groupby(level=0):
            logger.info(f"Processing data id: {id}")
            prompts_list = []
            for prompt, prompt_df in id_df.groupby(level=1):
                # logger.info(f"Processing prompt: {prompt}")
                # for prompt_idx, fact in prompt_df.iterrows():
                #     for model in self.ttsDict:
                #         logger.info(f"using Model: {model} for fact : {fact['Facts']}")
                #         self.ttsDict[model].create_audio(fact["Facts"])
                
                prompts_list.append(prompt)
                
            for model_tts in self.ttsDict:
                # self.ttsDict[model_tts].save_audio(f"{id}.wav")
            
                for model_ttv in self.ttvDict:
                    self.ttvDict[model_ttv].init(prompts_list)
                    self.ttvDict[model_ttv].add_audio(f"{self.config.get_config()['outPath']}/{model_tts}/{id}.wav")
                    self.ttvDict[model_ttv].create_video(prompts_list[0])
                    self.ttvDict[model_ttv].save_video(f"{id}.mp4")
        
    def get_tts_dict(self):
        return self.ttsDict
    
    def get_ttv_dict(self):
        return self.ttvDict0