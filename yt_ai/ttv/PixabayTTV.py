from yt_ai.utils.pixabay import pixabay as pb
from yt_ai.utils.audio import AudioData 
from yt_ai.utils.video import VideoData 
from random import shuffle
import soundfile as sf



class PixabayTTV():
    def __init__(self, config_file):
        self.config_file = config_file
        self.text = ""
        self.px = pb.core(config_file["ttv"]["PixabayTTV"]["token"])
        self.outputFilePath = config_file["filePath"]
        self.video = VideoData(self.outputFilePath, (512,512))
        self.data = []
        
    def get_videos(self, prompts=[], video_num = 20):
        data = []
        for prompt in prompts:        
            data.append(self.px.query(prompt))
        
        data = shuffle(data)
        if len(data) > video_num:
            data = data[:video_num]
        self.data = data
        
    def add_audio(self, audioPath):
        self.video.attach_audio(audioPath)
        
    def create_video(self, consider_audio = True):
        if consider_audio:
            if self.video.get_duration() > 0:
               audio_time_duration = self.video.get_duration()
               for video in self.data:
                   video_bytes = video.downloadRaw("large")
                   self.video.add_videos([video_bytes])
                   
                   if self.video.get_duration() > audio_time_duration:
                       break
                   
            else:
                raise Exception("No audio Found. please check") 
        else:
            video_byte_list = []
            for video in self.data:
                video_bytes = video.downloadRaw("large")
                video_byte_list.append(video_bytes)
            self.video.add_videos(video_byte_list)
    
    def save_video(self):
        self.video.save_video()