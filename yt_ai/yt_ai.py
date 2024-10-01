from yt_ai.utils.configreader import Config
from yt_ai.utils.logger import logger
import os

class Core:
    def __init__(self, config_file):
        self.config = Config(config_file)
        self.ttsDict = self.config.decode_tts()
        self.ttvDict = self.config.decode_ttv()
        
    def run(self):
        # Iterate over the data file
        for id, id_df in self.config.get_data().groupby(level=0):
            logger.info(f"Processing data id: {id}")
            prompts_list = []
            for prompt, prompt_df in id_df.groupby(level=1):
                prompts_list.append(prompt)
                
            for model_tts in self.ttsDict:
                # Generate audio
                audio_path = f"{self.config.get_config()['outPath']}/{model_tts}/{id}.wav"
                # Uncomment this if audio generation is needed
                # self.ttsDict[model_tts].save_audio(audio_path)
                
                for model_ttv in self.ttvDict:
                    # Initialize TTV model and create video
                    self.ttvDict[model_ttv].init(prompts_list)
                    self.ttvDict[model_ttv].add_audio(audio_path)
                    self.ttvDict[model_ttv].create_video(prompts_list[0])
                    
                    # Corrected video path (input video without subtitles)
                    video_path = f"{self.config.get_config()['outPath']}/PixabayTTV/{id}.mp4"
                    self.ttvDict[model_ttv].save_video(f"{id}.mp4")

                    # Apply subtitles directly and save as final video
                    subtitle_path = self.config.get_config()['dataFile']
                    output_path = f"{self.config.get_config()['outPath']}/PixabayTTV/{id}_final_with_subtitles.mp4"
                    self.config.apply_subtitles(video_path, subtitle_path, output_path)

                    # Remove the intermediate video without subtitles to save storage
                    os.remove(video_path)  # Removing the video without subtitles
                    logger.info(f"Removed the video without subtitles to save storage: {video_path}")
        
    def get_tts_dict(self):
        return self.ttsDict
    
    def get_ttv_dict(self):
        return self.ttvDict
