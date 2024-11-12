import logging
import uvicorn

from fastapi import FastAPI
from fastapi import FastAPI, HTTPException, Depends, status
from fastapi.security import OAuth2PasswordBearer

from api.v1 import chat,embeddings
from config import settings

app = FastAPI()

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

def verify_token(token: str = Depends(oauth2_scheme)):
    if token != settings.VALID_TOKEN:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or missing token",
            headers={"WWW-Authenticate": "Bearer"},
        )
    return token

app.include_router(chat.router, prefix="/chat", tags=["chat"], dependencies=[Depends(verify_token)])
app.include_router(embeddings.router, prefix="/embeddings", tags=["embeddings"], dependencies=[Depends(verify_token)])

if __name__ == "__main__":
    logging.basicConfig(
        level=logging.DEBUG, 
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
        handlers=[logging.FileHandler("ai_inference.log"), logging.StreamHandler()]
    )
    uvicorn.run(app, host=settings.HOST, port=settings.PORT)
