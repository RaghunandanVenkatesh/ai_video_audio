from yt_ai.utils.pixabay import pixabay as pb
from yt_ai.utils.audio import AudioData 
from yt_ai.utils.video import VideoData 
from random import shuffle
import tqdm
from yt_ai.utils.logger import logger
import time
from pathlib import Path
import os
from moviepy.editor import concatenate_videoclips, VideoFileClip
from moviepy.editor import AudioFileClip

class AudioData:
    def __init__(self, audio_path):
        self.audio_clip = AudioFileClip(audio_path)
    
    def get_duration(self):
        return self.audio_clip.duration
    
    def get_audio_clip(self):
        return self.audio_clip


class PixabayTTV():
    def __init__(self, c_fp):
        self.c_fp = c_fp  # config file
        self.text = ""
        self.px = pb.core(c_fp["ttv"]["PixabayTTV"]["token"])
        self.o_fp = Path(os.path.join(c_fp["outPath"], "PixabayTTV"))  # ensure proper path handling
        self.o_fp.mkdir(exist_ok=True, parents=True)
        self.video_clips = []
        
    def init(self, prompts=[], video_num=20):
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
        self.audio_path = audioPath
        
    def create_video(self, prompt="", consider_audio=True):
        if consider_audio:
            audioDur = AudioData(self.audio_path).get_duration()
            logger.info(f"Creating Video with Audio duration {audioDur}")
        else:
            logger.info(f"Creating Video without Audio")
            audioDur = 1e7
            
        videoDur = 0
        for videoH in self.data:
            qual = self.c_fp["ttv"]["PixabayTTV"]["quality"]
            if qual.lower() == "large":
                videoUrl = videoH.getVideoLarge()
            elif qual.lower() == "medium":
                videoUrl = videoH.getVideoMedium()
            else:
                videoUrl = videoH.getVideoSmall()
            if not videoUrl:
                continue
                
            # Load video clip using MoviePy
            videoClip = VideoFileClip(videoUrl)
            videoDur += videoClip.duration
            self.video_clips.append(videoClip)
            if videoDur >= audioDur:
                logger.info(f"Reached audio duration of {audioDur}")
                break
        
        final_clip = concatenate_videoclips(self.video_clips)
        final_clip = final_clip.subclip(0, audioDur)
        logger.info(f"video duration: {final_clip.duration}")
        final_clip = final_clip.set_audio(AudioFileClip(self.audio_path))
        
        self.final_clip = final_clip
        
    def save_video(self, f_name):
        logger.info(f"Saving video to {self.o_fp}/{f_name}")
        out_file = str(self.o_fp / f_name)
        self.final_clip.write_videofile(out_file)
        return out_file
