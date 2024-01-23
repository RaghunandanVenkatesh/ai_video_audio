import torch
from transformers import AutoTokenizer
from pathlib import Path
import json
import nltk
from nemo_text_processing.text_normalization.normalize import Normalizer
from nltk.tokenize import sent_tokenize, TweetTokenizer
from g2p_en import G2p
import soundfile as sf
import numpy as np
import gdown
from tqdm import tqdm
import re

def download_dependencies(model_path):
    nltk.download('punkt')
    out_dir = Path(model_path)
    # TODO change the download path
    if not (out_dir/"vocoder.pt").exists():
        gdown.download_folder("https://drive.google.com/drive/folders/1LVHA7L-qaPXuSgodxFQy3nrtsL5iqqiX?usp=sharing",verify=False ,use_cookies=False, output=str(out_dir))
    else:
        print("Google drive data already downloaded")



def split_arpabet(text):
    splits = re.finditer(r"{{(([^}][^}]?|[^}]}?)*)}}", text)
    out = []
    start = 0
    for split in splits:
        non_arpa = text[start:split.start()]
        arpa = text[split.start():split.end()]
        out = out + [non_arpa] + [arpa]
        start = split.end()
    if start < len(text):
        out.append(text[start:])
    return out

def split_context(text):
    splits = re.finditer(r"\[\[(([^\]][^\]]?|[^\]]\]?)*)\]\]", text)
    out = []
    start = 0
    """for split in splits:
        print(split)
        non_arpa = text[start:split.start()]
        arpa = text[split.start():split.end()]
        out = out + [non_arpa] + [arpa]
        start = split.end()
    if start < len(text):
        out.append(text[start:])"""
    return out

def is_arpabet(text):
    if len(text) < 4:
        return False
    return text[:2] == "{{" and text[-2:] == "}}" 

def is_context(text):
    if len(text) < 4:
        return False
    return text[:2] == "[[" and text[-2:] == "]]" 

def get_sentences(text):
    sentences = sent_tokenize(text)
    # ["What is this?", "?"] => ["What is this??"]
    merged_sentences = []
    for i, sentence in enumerate(sentences):
        if sentence in [".", "?", "!"]:
            continue
        for next_sentence in sentences[i + 1:]:
            if next_sentence in [".", "?", "!"]:
                sentence = sentence + next_sentence
            else:
                break
        merged_sentences.append(sentence)
    return merged_sentences