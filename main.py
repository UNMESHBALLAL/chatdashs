from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from transformers import AutoModelForCausalLM, AutoTokenizer
import torch
import uvicorn
from fastapi.middleware.cors import CORSMiddleware
import os
import json

# Initialize FastAPI app
app = FastAPI(title="Local GPT-2 API with Dashboard Generator")

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:4200", "http://127.0.0.1:4200", "http://localhost:4709"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Load the model and tokenizer once at startup
model_name = "HuggingFaceH4/zephyr-7b-beta"
MODEL_DIR = "./models"
os.makedirs(MODEL_DIR, exist_ok=True)

device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
print(f"🚀 Using device: {device}")

print("🚀 Loading tokenizer...")
tokenizer = AutoTokenizer.from_pretrained(
    model_name,
    cache_dir=MODEL_DIR,
    trust_remote_code=True,
    torch_dtype=torch.float16
)

print("🚀 Loading model...")
model = AutoModelForCausalLM.from_pretrained(
    model_name,
    cache_dir=MODEL_DIR,
    device_map="auto",
    torch_dtype=torch.float16,
    trust_remote_code=True
)
model.to(device)
print("✅ Model loaded successfully")

if tokenizer.pad_token is None:
    tokenizer.pad_token = tokenizer.eos_token


# ================== Pydantic Schemas ===================
class PromptRequest(BaseModel):
    prompt: str
    max_length: int = 100


class DashboardRequest(BaseModel):
    instruction: str
    max_length: int = 500


# ================== Routes ===================
@app.post("/generate")
def generate_text(request: PromptRequest):
    try:
        inputs = tokenizer(request.prompt, return_tensors="pt").to(device)
        outputs = model.generate(
            inputs["input_ids"],
            max_length=request.max_length,
            num_return_sequences=1,
            temperature=0.7,
            do_sample=True,
            pad_token_id=tokenizer.eos_token_id
        )
        response = tokenizer.decode(outputs[0], skip_special_tokens=True)
        return {"generated_text": response}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/generate_dashboard")
def generate_dashboard(request: DashboardRequest):
    """
    Generate dashboard + dashlets JSON from text instruction.
    """
    try:
        # Few-shot prompt to enforce JSON output
        example_json = """
        {
            "dashboardName": "Query based Dashboard",
            "description": "Sample Dashboard.",
            "dashboardId": 1,
            "permission": "RW",
            "Owner": "admin",
            "shared_with": ["Swarna", "demo"],
            "dashlets": [
                {
                    "widgetTitle": "Sales Trends",
                    "widgetTypeName": "Line Chart",
                    "measurements": "value",
                    "time_interval": "1 Year",
                    "refreshTime": 30,
                    "dataSource": "sales_data"
                }
            ]
        }
        """

        prompt = f"""
        You are a JSON generator for dashboards. 
        Based on the following user request, generate ONLY valid JSON (no extra text).

        Example format: {example_json}

        User request: {request.instruction}
        """

        inputs = tokenizer(prompt, return_tensors="pt").to(device)
        outputs = model.generate(
            inputs["input_ids"],
            max_length=request.max_length,
            temperature=0.6,
            do_sample=True,
            pad_token_id=tokenizer.eos_token_id
        )
        response = tokenizer.decode(outputs[0], skip_special_tokens=True)

        # Try to parse JSON
        try:
            dashboard_json = json.loads(response)
        except json.JSONDecodeError:
            raise HTTPException(status_code=500, detail="Model did not return valid JSON")

        return {"dashboard": dashboard_json}

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/")
def read_root():
    return {"message": "Zephyr-7B API is running!", "status": "healthy"}


@app.get("/health")
def health_check():
    return {"status": "healthy", "model": model_name}


if __name__ == "__main__":
    print("🎯 Starting FastAPI server on http://127.0.0.1:8000")
    uvicorn.run(app, host="127.0.0.1", port=8000)
