from fastapi import FastAPI
from pydantic import BaseModel
from sentence_transformers import SentenceTransformer
from typing import List

class EmbeddingsRequest(BaseModel):
    prompt: str
    model: str
    encoding_format: str

class EmbeddingsResponse(BaseModel):
    embeddings: List[float]

app = FastAPI()

model = SentenceTransformer("/workspace/model/embedding/bge-large-en-v1.5")
@app.post("/embeddings",response_model=EmbeddingsResponse)
def embedding(request:EmbeddingsRequest):
    print(f" request model:{request.model} encoding_format:{request.encoding_format} prompt: {request.prompt}")
    encodes = model.encode([request.prompt], normalize_embeddings=True).tolist()
    print(f"{encodes[0]}")
    return EmbeddingsResponse(embeddings=encodes[0])