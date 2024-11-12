import os
import argparse
import uvicorn
from fastapi import FastAPI
from pydantic import BaseModel
from sentence_transformers import SentenceTransformer
from typing import List


app = FastAPI()
model = None

class EmbeddingsRequest(BaseModel):
    prompt: str
    model: str
    encoding_format: str

class EmbeddingsResponse(BaseModel):
    embeddings: List[float]

def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('--model', type=str, default='bge-large-en-v1.5', help='The model name')
    parser.add_argument('--port', type=int, default=8010, help='The model port')
    return parser.parse_args()

def load_model(model_name: str):
    global model
    model_path = f"/workspace/model/{model_name}"
    if not os.path.exists(model_path):
        raise FileNotFoundError(f"Model not found at {model_path}")
    model = SentenceTransformer(model_path)
    print(f"Loaded model from {model_path}")

@app.on_event("startup")
def startup_event():
    args = parse_args()
    load_model(args.model)


@app.post("/embeddings",response_model=EmbeddingsResponse)
def embedding(request:EmbeddingsRequest):
    print(f" request model:{request.model} encoding_format:{request.encoding_format} prompt: {request.prompt}")
    encodes = model.encode([request.prompt], normalize_embeddings=True).tolist()
    return EmbeddingsResponse(embeddings=encodes[0])

if __name__ == "__main__":  
    args = parse_args()
    uvicorn.run("main:app", host="0.0.0.0", port=args.port, reload=False)