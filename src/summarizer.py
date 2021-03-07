"""
    An REST API for news summarization
"""
import math

from flask import Flask, jsonify, request

import torch
from transformers import AutoTokenizer, AutoModelForSeq2SeqLM
from transformers import BartForConditionalGeneration, BartTokenizer


MAX_LENGTH = 1024
DEVICE = "cuda" if torch.cuda.is_available() else "cpu"
tokenizer = None
model = None
app = Flask(__name__)


@app.route("/summarize", methods=["POST"])
def summarize():
    data = {"success": False}

    if request.method == "POST":
        news = request.get_json()
        content = news["content"]
        content_length = len(news["content"])

        contents = []
        if content_length > MAX_LENGTH:
            split_times = math.ceil(content_length / MAX_LENGTH)
            split_size = int(content_length/split_times)

            for idx in range(split_times):
                if idx + 1 == split_times:  # if last
                    contents.append(content[split_size*idx :])
                else:
                    contents.append(content[split_size*idx : split_size*(idx + 1)])
        else:
            contents.append(content)

        # assume there is only one news here
        batch = tokenizer.prepare_seq2seq_batch(contents, truncation=False, padding='longest', return_tensors="pt").to(DEVICE)

        summary = model.generate(**batch)
        summary = tokenizer.batch_decode(summary, skip_special_tokens=True)
        
        data["id"] = news["id"]
        data["summary"] = summary[0] if content_length <= MAX_LENGTH else " ".join(summary)
        data["success"] = True

    return jsonify(data)


def load_model():
    global tokenizer, model
    tokenizer = AutoTokenizer.from_pretrained("google/pegasus-cnn_dailymail")  
    model = AutoModelForSeq2SeqLM.from_pretrained("google/pegasus-cnn_dailymail").to(DEVICE)


if __name__=='__main__':
    load_model()
    app.run()