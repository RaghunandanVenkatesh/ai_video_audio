from IPython.display import HTML
from base64 import b64encode
from moviepy.editor import VideoFileClip, concatenate_videoclips, ColorClip, AudioFileClip, CompositeVideoClip
import numpy as np


def visualize_video_colab(video_path):
    mp4 = open(video_path,'rb').read()
    data_url = "data:video/mp4;base64," + b64encode(mp4).decode()
    return HTML("""
    <video width=400 controls>
        <source src="%s" type="video/mp4">
    </video>
    """ % data_url)

class VideoData:
    def __init__(self, outputfp, size):
        self.outputfp = outputfp
        self.video = ColorClip(size, duration=0.01)
        self.audiofp = ""
        
    def add_videos(self, videoList = []):
        for video in videoList:
            videoclip = VideoFileClip(video)
            self.video = concatenate_videoclips([self.video, videoclip])
    
    def merge_videos(self, videoList = []):
        for video in videoList:
            videoclip = VideoFileClip(video) 
            self.video = CompositeVideoClip([self.video, videoclip])  
        
    def attach_audio(self, audiofp):
        self.audiofp = audiofp
        self.video.set_audio(AudioFileClip("allwell.mp3"))
    
    def save_video(self):
        self.video.write_videofile(self.outputfp)
    
    def set_fps(self, fps):
        self.video.set_fps(fps)
        
    def get_fps(self):
        return self.video.fps
    
    def get_audio(self):
        return self.video.audio.to_numpy()
    
    def get_output_folder(self):
        return self.outputfp
    
    def get_video(self):
        return np.array(list(self.video.iter_frames()))
    
    def get_audio_path(self):
        return self.audiofp
