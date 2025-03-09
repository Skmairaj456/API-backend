

from fastapi import FastAPI, WebSocket
from transformers import pipeline
import os
import ssl


try:
    ssl.create_default_context()
except AttributeError:
    raise ImportError("SSL module is not available. Ensure your Python installation includes SSL support.")

app = FastAPI()


ai_model = pipeline("text-generation", model="bigcode/starcoder")

@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    while True:
        user_input = await websocket.receive_text()
        response = ai_model(user_input, max_length=200)[0]['generated_text']
        await websocket.send_text(response)


