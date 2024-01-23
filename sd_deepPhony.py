
import tts
import tqdm
import ipywidgets as widgets
import json
from scipy.io.wavfile import write
import numpy as np
from stable_diffusion_videos import StableDiffusionWalkPipeline, Interface
import torch

# init deep phony
tts_ = tts.DeepPoniesTTS()

# init sd
pipeline = StableDiffusionWalkPipeline.from_pretrained(
    "CompVis/stable-diffusion-v1-4",
    torch_dtype=torch.float16,
    revision="fp16",
).to("cuda")

interface = Interface(pipeline)