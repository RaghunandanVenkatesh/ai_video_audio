import utils.pixabay as pb
from utils.audio import AudioData 
from utils.video import VideoData 
from random import shuffle
import soundfile as sf



class PixabayTTV():
    def __init__(self, token):
        self.text = ""
        self.px = pb.core(token)
        self.audioFilePath = ""
        self.outputFilePath = ""
        self.audioData = AudioData(self.audioFilePath)
        self.video = VideoData("videofile.mp4", (512,512))
        self.data = []
        
    def get_video(self, prompts=[], video_num = 20):
        data = []
        for prompt in prompts:        
            data.append(self.px.query(prompt))
        
        data = shuffle(data)
        if len(data) > video_num:
            data = data[:video_num]
        self.data = data
        
    def add_audio(self, audioPath):
        self.audioFilePath = audioPath
        self.audioData = AudioData(self.audioFilePath)
        
    def create_video(self, consider_audio = True):
        
        