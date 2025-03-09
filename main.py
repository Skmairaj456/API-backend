from fastapi import FastAPI, WebSocket
from transformers import pipeline, AutoModelForCausalLM, AutoTokenizer
import os

app = FastAPI()

# Use a smaller model for Render free-tier (512MB limit)
MODEL_NAME = os.getenv("MODEL_NAME", "distilgpt2")

try:
    tokenizer = AutoTokenizer.from_pretrained(MODEL_NAME)
    model = AutoModelForCausalLM.from_pretrained(MODEL_NAME)
    ai_model = pipeline("text-generation", model=model, tokenizer=tokenizer)
    print(f"✅ Successfully loaded model: {MODEL_NAME}")
except Exception as e:
    print(f"❌ Error loading model: {e}")
    ai_model = None  # Prevent crashes

@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    while True:
        user_input = await websocket.receive_text()
        
        if ai_model:
            response = ai_model(user_input, max_length=100)[0]['generated_text']
        else:
            response = "⚠️ AI model failed to load. Please check server logs."
        
        await websocket.send_text(response)

# Run this with: uvicorn main:app --host 0.0.0.0 --port 8000
