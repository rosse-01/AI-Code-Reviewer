from fastapi import FastAPI
from pydantic import BaseModel
import torch
from transformers import AutoModelForCausalLM, AutoTokenizer
import os
from pathlib import Path

app = FastAPI(
    title="Qwen2.5 Code Reviewer API",
    description="Production-ready microservice for automated code reviews.",
    version="1.0"
)

from tokenizers import Tokenizer
from transformers import PreTrainedTokenizerFast

MODEL_PATH = "/workspace/app/model_files"

print("Loading model and tokenizer into memory")

backend_tokenizer = Tokenizer.from_file(f"{MODEL_PATH}/tokenizer.json")

tokenizer = PreTrainedTokenizerFast(tokenizer_object=backend_tokenizer)
tokenizer.pad_token = tokenizer.eos_token

tokenizer.chat_template = (
    "{% for message in messages %}"
    "{{ '<|im_start|>' + message['role'] + '\n' + message['content'] + '<|im_end|>\n' }}"
    "{% endfor %}"
    "{% if add_generation_prompt %}"
    "{{ '<|im_start|>assistant\n' }}"
    "{% endif %}"
)

model = AutoModelForCausalLM.from_pretrained(
    MODEL_PATH, 
    torch_dtype=torch.bfloat16,
)
device = "cuda" if torch.cuda.is_available() else "cpu"
model = model.to(device)

print("Model loaded successfully, API is live.")

# Define data payload structure using Pydantic
class CodeInput(BaseModel):
    code: str

# basic health check endpoint
@app.get("/")
def health_check():
    return {"status": "healthy", "model": "Qwen2.5-Coder-3B-FineTuned"}

# core prediction endpoint
@app.post("/review")
def review_code(payload: CodeInput):
    messages = [
        {"role": "system", "content": "You are an expert software engineer and code reviewer."},
        {"role": "user", "content": f"Analyze this code for bugs, architectural design issues, and optimizations:\n\n{payload.code}"}
    ]
    
    # Render the input strings into formatting tokens the model understands
    text = tokenizer.apply_chat_template(messages, tokenize=False, add_generation_prompt=True)
    inputs = tokenizer([text], return_tensors="pt").to(model.device)
    
    # Run token generation
    with torch.no_grad():
        generated_ids = model.generate(
            input_ids=inputs.input_ids,
            attention_mask=inputs.attention_mask,
            max_new_tokens=512,
            temperature=0.4,
            do_sample=True, # Required if specifying a temperature configuration
            pad_token_id=tokenizer.pad_token_id
        )
        
    generated_ids = [ids[len(inputs.input_ids[0]):] for ids in generated_ids]
    review_output = tokenizer.decode(generated_ids[0], skip_special_tokens=True)
    
    return {"review": review_output}
