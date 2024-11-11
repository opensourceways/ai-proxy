from fastapi import APIRouter
import requests

from model import chat_model
from config import settings

router = APIRouter()

@router.post("/completions")
def completions(request: chat_model.ChatRequest): 
    print(f" request model:{request.model} max_token:{request.max_tokens} temperature:{request.temperature} prompt: {request.prompt}")
    if request.model not in settings.PORT_DICT:
        return  f"model not found"

    url = f"http://localhost:{settings.PORT_DICT[request.model]}/v1/completions"
    headers = {
            "Content-Type": "application/json"
    }
    print(f"url: {url}")
    response = requests.post(url, headers=headers, json=request.to_dict())
    print(f" response model:{request.model}")
    if response.status_code == 200:
        return response.json()
    else:
        print("Request failed with status code:", response.status_code)
        print("Error response:", response.text)
        return None
    
