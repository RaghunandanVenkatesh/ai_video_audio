import torch
from transformers import AutoTokenizer
from pathlib import Path
import json
from nemo_text_processing.text_normalization.normalize import Normalizer
from nltk.tokenize import sent_tokenize, TweetTokenizer
from g2p_en import G2p
import soundfile as sf
import numpy as np
from tqdm import tqdm
from yt_ai.tts.utils.DeepPoniesTTS import *
import os
os.environ['CURL_CA_BUNDLE'] = ''

class DeepPoniesTTS():
    def __init__(self, config_file):
        self.confile_file = config_file
        model_path = os.environ['HF_DATASETS_CACHE']+"/DeepPoniesTTS"
        download_dependencies(model_path)
        self.g2p = G2p()
        self.acoustic_model = torch.jit.load(Path(model_path) / "acoustic_model.pt")
        self.style_predictor = torch.jit.load(Path(model_path) / "style_predictor.pt")        
        self.vocoder = torch.jit.load(Path(model_path)  / "vocoder.pt")
        self.tokenizer = AutoTokenizer.from_pretrained("prajjwal1/bert-tiny", verify=False)
        self.normalizer = Normalizer(input_case='cased', lang='en')
        self.speaker2id = self.get_speaker2id()
        self.symbol2id = self.get_symbol2id()
        self.lexicon = self.get_lexicon()
        self.word_tokenizer = TweetTokenizer()
        self.acoustic_model.eval()
        self.style_predictor.eval()
        self.vocoder.eval()

    def get_speaker2id(self):
        speaker2id = {}
        with open(Path(__file__).parent / "assests/DeepPoniesTTS" / "speakerCategories.json", "r") as json_file:
            data = json.load(json_file)
        for category in data.keys():
            for item in data[category]["items"]:
                if not item["activated"]:
                    continue
                speaker2id[item["speaker"]] = item["speaker_id"]
        return speaker2id

    def get_symbol2id(self):
        with open(Path(__file__).parent / "assests/DeepPoniesTTS"/ "symbol2id.json", "r") as json_file:
            symbol2id = json.load(json_file)
        return symbol2id

    def get_lexicon(self):
        dic = {}
        with open(Path(__file__).parent / "assests/DeepPoniesTTS" / "lexicon.txt", "r") as f:
            lines = f.readlines()
        for line in lines:
            split = line.rstrip().split(" ")
            text = split[0].strip()
            phones = split[1:]
            dic[text] = phones
        return dic

    def synthesize(self, text: str, speaker_name: str, duration_control: float=1.0, verbose: bool=True) -> np.ndarray:
        waves = []
        text = text.strip()
        speaker_ids = torch.LongTensor([self.speaker2id[speaker_name]]) 
        if text[-1] not in [".", "?", "!"]:
            text = text + "."

        sentences = get_sentences(text)
        if verbose:
            sentences = tqdm(sentences)
        for sentence in sentences:
            phone_ids = []
            subsentences_style = []
            for subsentence in split_arpabet(sentence):
                if is_arpabet(subsentence):
                    for phone in subsentence.strip()[2:-2].split(" "):
                        if "@" + phone in self.symbol2id:
                            phone_ids.append(self.symbol2id["@" + phone])
                else:
                    subsentences_style.append(subsentence)
                    subsentence = self.normalizer.normalize(subsentence, verbose=False)
                    for word in self.word_tokenizer.tokenize(subsentence):
                        word = word.lower()
                        if word in [".", "?", "!"]:
                            phone_ids.append(self.symbol2id[word])
                        elif word in [",", ";"]:
                            phone_ids.append(self.symbol2id["@SILENCE"])
                        elif word in self.lexicon:
                            for phone in self.lexicon[word]:
                                phone_ids.append(self.symbol2id["@" + phone])
                            phone_ids.append(self.symbol2id["@BLANK"])
                        else:
                            for phone in self.g2p(word):
                                phone_ids.append(self.symbol2id["@" + phone])
                            phone_ids.append(self.symbol2id["@BLANK"])
            
            subsentence_style = " ".join(subsentences_style)
            encoding = self.tokenizer(
                subsentence_style,
                add_special_tokens=True,
                padding=True, 
                return_tensors="pt"
            )
            input_ids = encoding["input_ids"]
            attention_mask = encoding["attention_mask"]
            phone_ids = torch.LongTensor([phone_ids])
            with torch.no_grad():
                style = self.style_predictor(input_ids, attention_mask)
                mels = self.acoustic_model(
                    phone_ids,
                    speaker_ids,
                    style,
                    1.0,
                    duration_control
                )
                wave = self.vocoder(mels, speaker_ids, torch.FloatTensor([1.0]))
                waves.append(wave.view(-1))
        full_wave = torch.cat(waves, dim=0).cpu().numpy()
        return full_wave
    
if __name__ == "__main__":
    tts = DeepPoniesTTS()
    audio = tts.synthesize("Wouldn't that be great!", "Heavy")
    # audio = tts.synthesize("Wouldn't that be great!!", "Heavy")
    sf.write("audio.wav", audio, 22050)