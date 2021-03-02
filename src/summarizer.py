from flask import Flask, jsonify, request

import torch
from transformers import AutoTokenizer, AutoModelForSeq2SeqLM
from transformers import BartForConditionalGeneration, BartTokenizer


DEVICE = "cuda" if torch.cuda.is_available() else "cpu"
tokenizer = None
model = None
app = Flask(__name__)


@app.route("/summarize", methods=["POST"])
def summarize():
    data = {"success": False}

    if request.method == "POST":
        news = request.get_json()
        print(news["id"])
        
        # assume there is only one news here
        batch = tokenizer.prepare_seq2seq_batch(news["content"], truncation=True, padding='longest', return_tensors="pt").to(DEVICE)
        translated = model.generate(**batch)
        tgt_text = tokenizer.batch_decode(translated, skip_special_tokens=True)
        
        data["id"] = news["id"]
        data["summary"] = tgt_text
        data["success"] = True

    return jsonify(data)


def load_model():
    global tokenizer, model
    tokenizer = AutoTokenizer.from_pretrained("google/pegasus-newsroom")  
    model = AutoModelForSeq2SeqLM.from_pretrained("google/pegasus-newsroom").to(DEVICE)


if __name__=='__main__':
    load_model()
    app.run()