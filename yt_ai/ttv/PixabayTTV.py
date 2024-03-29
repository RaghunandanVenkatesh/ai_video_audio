from yt_ai.utils.pixabay import pixabay as pb
from yt_ai.utils.audio import AudioData 
from yt_ai.utils.video import VideoData 
from random import shuffle
import soundfile as sf
import tqdm
from yt_ai.utils.logger import logger
import time
from pathlib import Path

class PixabayTTV():
    def __init__(self, c_fp):
        self.c_fp = c_fp # config file
        self.text = ""
        self.px = pb.core(c_fp["ttv"]["PixabayTTV"]["token"])
        self.o_fp = Path(c_fp["outPath"] + "/PixabayTTV") # output folder
        self.o_fp.mkdir(exist_ok=True, parents=True)
        self.video = VideoData((self.c_fp["width"], self.c_fp["height"]))
        self.data = []
        
    def init(self, prompts=[], video_num = 20):
        data = []
        for prompt in prompts:
            logger.info(f"Initializing for prompt: {prompt}")
            for idx, video in tqdm.tqdm(enumerate(self.px.queryVideo(prompt))):
                if idx > video_num:
                    break
                data.append(video)
                time.sleep(0.01)    
        
        shuffle(data)
        if len(data) > video_num:
            data = data[:video_num]
        self.data = data
        
    def add_audio(self, audioPath):
        logger.info(f"Adding audio to video from {audioPath}")
        self.video.attach_audio(audioPath)
        
    def create_video(self, prompt = "" ,consider_audio = True):

        if consider_audio:
            audioDur = self.video.get_audio_duration()
            logger.info(f"Creating Video with Audio duration {audioDur}")
        else:
            logger.info(f"Creating Video without Audio")
            audioDur = 1e7
            
        videos = []
        videoDur = 0
        for videoH in self.data:
            qual = self.c_fp["ttv"]["PixabayTTV"]["quality"]
            if qual.lower() == "large":
                videoUrl = videoH.getVideoLarge()
            elif  qual.lower() == "medium":
                videoUrl = videoH.getVideoMedium()
            else:
                videoUrl = videoH.getVideoSmall()
            if not videoUrl:
                continue
            videoDur += videoH.getDuration()
            videos.append(videoUrl)
            
            if videoDur > audioDur:
                break
        self.video.add_videos(videos)
    
        if prompt:
            self.video.add_text(prompt=prompt)
        logger.info("Creating video completed")
    
    def save_video(self, outputfp):
        logger.info(f"saving video to {self.o_fp}/{outputfp}")
        self.video.save_video(f"{self.o_fp}/{outputfp}")