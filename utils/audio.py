import soundfile as sf

class AudioData:
    def __init__(self, audiofp = ""):
        self.audiofp = audiofp
        self.audio = sf.SoundFile(self.audiofp)
        
    def get_audio(self):
        return self.audio
    
    def get_samples(self):
        return self.audio.frames
    
    def get_samplerate(self):
        return self.audio.samplerate
    
    def get_duration(self):
        return self.audio.frames/self.audio.samplerate
    
    def get_audio_file_path(self):
        return self.audiofp