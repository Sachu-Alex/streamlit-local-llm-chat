# api.py
from fastapi import FastAPI, Request
from pydantic import BaseModel
import requests

app = FastAPI()

OLLAMA_API_URL = "http://localhost:11434/api/generate"
MODEL_NAME = "llama3"  # Or your preferred model


class PromptRequest(BaseModel):
    prompt: str


@app.post("/generate")
def generate(prompt_req: PromptRequest):
    prompt = prompt_req.prompt
    response = requests.post(
        OLLAMA_API_URL,
        json={
            "model": MODEL_NAME,
            "prompt": prompt,
            "stream": False
        }
    )
    response.raise_for_status()
    return {"response": response.json()["response"]}
