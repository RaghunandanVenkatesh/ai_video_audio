import json
import importlib
import os
from yt_ai.utils.logger import logger
from yt_ai.utils.datareader import read_data_csv
from moviepy.config import change_settings
from moviepy.editor import VideoFileClip, TextClip, CompositeVideoClip
import csv

class Config:
    def __init__(self, configFile):
        self.configFile = configFile
        logger.info(f"Reading Config file from {configFile}")
        with open(self.configFile, "r") as f:
            self.config = json.load(f)
        
        os.environ['CURL_CA_BUNDLE'] = ''
        change_settings({"IMAGEMAGICK_BINARY": r"C:\Program Files\ImageMagick-7.1.1-Q16-HDRI\magick.exe"})
        
        logger.debug(f"Setting cache folder: {self.config['cache']}")
        os.environ['HF_DATASETS_CACHE'] = self.config["cache"]
        if self.config["use_cpu"]:
            os.environ["CUDA_VISIBLE_DEVICES"] = ""
            os.environ["SUNO_OFFLOAD_CPU"] = "True"
            os.environ["SUNO_USE_SMALL_MODELS"] = "True"
        
        self.data = read_data_csv(self.config["dataFile"])
        self.ensure_output_directories()

    def ensure_output_directories(self):
        """Ensure that the output directories exist."""
        out_path = self.config.get('outPath', 'output')
        pixabay_dir = os.path.join(out_path, 'PixabayTTV')
        final_dir = os.path.join(out_path, 'final_videos')

        if not os.path.exists(pixabay_dir):
            os.makedirs(pixabay_dir)
            logger.info(f"Created directory: {pixabay_dir}")

        if not os.path.exists(final_dir):
            os.makedirs(final_dir)
            logger.info(f"Created directory: {final_dir}")

    def decode_tts(self):
        ttsDict = {}
        for model in self.config["tts"]:
            logger.info(f"Loading tts model: {model}")
            module = importlib.import_module(f'yt_ai.tts.{model}')
            ttsDict[model] = getattr(module, f"{model}")(self.config)
        return ttsDict

    def decode_ttv(self):
        ttvDict = {}
        for model in self.config["ttv"]:
            logger.info(f"Loading ttv model: {model}")
            module = importlib.import_module(f'yt_ai.ttv.{model}')
            ttvDict[model] = getattr(module, f"{model}")(self.config)
        return ttvDict

    def apply_subtitles(self, video_path, subtitle_path, output_path):
        # Log the video path for verification
        logger.info(f"Applying subtitles to video: {video_path}")

        # Ensure the path exists before processing
        if not os.path.exists(video_path):
            raise FileNotFoundError(f"Video file not found at path: {video_path}")

        # Proceed with processing the video with subtitles
        video = VideoFileClip(video_path)

        subtitles = []
        with open(subtitle_path, newline='') as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                fact = row['Facts']
                start_time = float(row['Start Time'])
                end_time = float(row['End Time'])

                # Adjust font size based on video resolution
                font_size = max(int(video.size[0] * 0.035), 24)  # 3% of video height or minimum 24

                # Position subtitle in the center of the video
                subtitle = TextClip(fact, fontsize=font_size, font="Arial", color='white')
                subtitle = subtitle.set_position(('center', 'center')).set_duration(end_time - start_time)
                subtitle = subtitle.set_start(start_time)

                subtitles.append(subtitle)

        final = CompositeVideoClip([video] + subtitles)
        final.write_videofile(output_path, fps=video.fps)

    def get_config(self):
        return self.config

    def get_data(self):
        return self.data
