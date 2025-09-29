from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
#import inspect2 as inspect

from transformers import AutoModelForCausalLM, AutoTokenizer
import torch

# Initialize FastAPI app
app = FastAPI(title="Local GPT-2 API")

# Load the model and tokenizer once at startup
model_name = "gpt2"
tokenizer = AutoTokenizer.from_pretrained(model_name)
model = AutoModelForCausalLM.from_pretrained(model_name)

device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
model.to(device)

# Define request body
class PromptRequest(BaseModel):
    prompt: str
    max_length: int = 50  # Optional: allow custom generation length

@app.post("/generate")
def generate_text(request: PromptRequest):
    try:
        inputs = tokenizer(request.prompt, return_tensors="pt").to(device)
        outputs = model.generate(
            inputs["input_ids"],
            max_length=request.max_length,
            do_sample=True
        )
        response = tokenizer.decode(outputs[0], skip_special_tokens=True)
        return {"generated_text": response}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    