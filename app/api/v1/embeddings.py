import requests
from fastapi import APIRouter

from model import embeddings_model
from config import settings


router = APIRouter()

@router.post("")
def embedding(request: embeddings_model.EmbeddingsRequest):
    print(f" request model:{request.model} encoding_format:{request.encoding_format} prompt: {request.prompt}")
    if request.model not in settings.PORT_DICT:
        return  f"model not found"

    url = f"http://127.0.0.1:{settings.PORT_DICT[request.model]}/embeddings"
    headers = {
            "Content-Type": "application/json"
    }
    print(f"url: {url}")
    response = requests.post(url, headers=headers, json=request.to_dict())
    print(f" response model:{request.model} ")
    if response.status_code == 200:
        return response.json()
    else:
        print("Request failed with status code:", response.status_code)
        print("Error response:", response.text)
        return None