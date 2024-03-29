from IPython.display import HTML
from base64 import b64encode
from moviepy.editor import VideoFileClip, CompositeAudioClip, TextClip
from moviepy.editor import concatenate_videoclips, ColorClip, AudioFileClip, CompositeVideoClip
import numpy as np
from yt_ai.utils.logger import logger

def visualize_video_colab(video_path):
    mp4 = open(video_path,'rb').read()
    data_url = "data:video/mp4;base64," + b64encode(mp4).decode()
    return HTML("""
    <video width=400 controls>
        <source src="%s" type="video/mp4">
    </video>
    """ % data_url)

class VideoData:
    def __init__(self,  size):
        self.video = ColorClip(size, color=(0,0,0), duration=0.01)
        self.audiofp = ""
        self.audioClip = None
        self.size = size
        
    def add_videos(self, videos = []):
        logger.debug(f"Concatinating {len(videos)} videos")
        
        for video in videos:
            videoclip = VideoFileClip(video)
            self.video = concatenate_videoclips([self.video, videoclip], method="compose")
    
    def merge_videos(self, videos = []):
        for video in videos:
            videoclip = VideoFileClip(video) 
            self.video = CompositeVideoClip([self.video, videoclip])  
        
    def attach_audio(self, audiofp):
        self.audiofp = audiofp
        self.audioClip = AudioFileClip(self.audiofp)
    
    def save_video(self, outputfp, fps = 10):
        if self.audioClip is not None:
            new_audioclip = CompositeAudioClip([self.audioClip])
            self.video.audio = new_audioclip
            # self.video.set_audio(self.audioClip)
        self.video.write_videofile(outputfp, fps = fps, threads=4)
    
    def text_creator_(self, text_data, duration, font_name = 'Arial', font_size=15, stroke_width=15, inner_color="black", bg_colour="white"):
        """
        creates a text data with required font
        TextClip.list('font')
        TextClip.list('color')

        """
        txtClp = TextClip(text_data, font=font_name ,fontsize = font_size,color=inner_color,stroke_color=bg_colour, stroke_width=stroke_width)
        # Set the duration for the text clip
        txtClp = txtClp.set_duration(duration)
        txtClp = txtClp.set_position(('center', 'center'))
        # Get the initial dimensions (width and height) of the text clip
        textW, textH = txtClp.size

        # 3. Define the Resize (Scaling) Function
        def resize_(t, height, width):
            # ending scale factor
            es = 1
            # End scale factor (the size to which the text should grow)
            esH = height / textH
            esW = width / textW
            ss = min(esH, esW) * 0.5 # start scale

            # Calculate the scaling factor based on elapsed time and total duration
            sf = ss + t/duration * (es - ss)
            return sf

        # 4. Apply the Resize Effect to the Text
        # Resize the text over time using the scaling function
        txtAnim = txtClp.resize(lambda t: resize_(t, self.size[0], self.size[1]))
        txtAnim.set_start(5)
        return txtAnim

    def add_text(self, prompt):
        txtAnimBg = self.text_creator_(prompt.strip("\n"), 5, "Arial",20, 15, 'black', 'white')
        txtAnim = self.text_creator_(prompt.strip("\n"), 5, "Arial", 20, 1, 'black', None)
        # Overlay the resized text on the background to create a composite video
        self.video = CompositeVideoClip([self.video, txtAnimBg, txtAnim])
                    
    def set_fps(self, fps):
        self.video.set_fps(fps)
        
    def get_fps(self):
        return self.video.fps
    
    def get_audio_duration(self):
        return self.audioClip.duration
    
    def get_video_duration(self):
        return self.video.duration
    
    def get_audio(self):
        return self.video.audio.to_numpy()
    
    def get_output_folder(self):
        return self.outputfp
    
    def get_video(self):
        return np.array(list(self.video.iter_frames()))
    
    def get_audio_path(self):
        return self.audiofp
