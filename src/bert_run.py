# -*- coding: utf-8 -*-
import os
import sys
import time
import pathlib
import torch
import onnxruntime
import numpy as np
abs_path = pathlib.Path(__file__).parent.absolute()
sys.path.append(sys.path.append(abs_path))
import torch.nn.functional as F
from transformers import BertTokenizer


class Model(object):
    def __init__(self, config):
        self.config = config
        self.tokenizer = BertTokenizer.from_pretrained(config["MODEL_PATH"])
        self.model_name = os.path.join(config["MODEL_PATH"], 
                                        config["MODEL_NAME"])
        self.session = self.load_model()
        self.inp_name =  self.session.get_inputs()[0].name
        self.mask_name = self.session.get_inputs()[1].name
        
    def load_model(self):
        session = onnxruntime.InferenceSession(self.model_name)
        return session

    def build_tensor(self, s):
        pad_size = self.config.get("PAD_SIZE")
        #device = self.config.device
        inputs_dict = self.tokenizer.encode_plus(s,
                                            padding='max_length',
                                            truncation=True,
                                            max_length=pad_size,  
                                            pad_to_max_length=True, 
                                            return_attention_mask=True,
                                            return_tensors="pt")
        input_ids = inputs_dict['input_ids']
        attention_mask = inputs_dict['attention_mask']
        return input_ids, attention_mask
        
    def predict(self, s):
        if len(s.strip()) == 0:
            return 0, 0.0
        input_ids, attention_mask = self.build_tensor(s)
        out = self.session.run(None, {self.inp_name: input_ids.cpu().numpy(), 
                                self.mask_name: attention_mask.cpu().numpy()})
        print("out:", out)
        pred_softmax = F.softmax(torch.from_numpy(out[0]), dim=1)
        prob = pred_softmax[::, 1].item()
        return prob   


if __name__ == "__main__":
    conf = {
        "MODEL_PATH": "../data/bert_model/bert",
        "MODEL_NAME": "roberta.pt",
        "DEVICE": "cpu",
        "PAD_SIZE": 128,
        "RATE": 0.5
    }
    model = Model(conf)
    s = "就是你们在打分的时候，对方会手会放在哪里好放放哪，不会举着手吧哈，嗯，摁头要靠哪头？我操我头我的妈哇的哇。"
    print(model.predict(s))
