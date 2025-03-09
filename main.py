from fastapi import FastAPI, WebSocket
from transformers import pipeline
import os

app = FastAPI()

# Load AI model (Use GPT-2 for testing; StarCoder might be too large for free-tier hosting)
MODEL_NAME = os.getenv("MODEL_NAME", "gpt2")  # Change this to "bigcode/starcoder" when using a powerful server

ai_model = pipeline("text-generation", model=MODEL_NAME)

@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    while True:
        user_input = await websocket.receive_text()
        response = ai_model(user_input, max_length=200)[0]['generated_text']
        await websocket.send_text(response)

# Run: uvicorn main:app --host 0.0.0.0 --port 8000

