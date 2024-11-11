import uvicorn

from fastapi import FastAPI

from api.v1 import chat,embeddings
from config import settings

app = FastAPI()

app.include_router(chat.router, prefix="/chat", tags=["chat"])
app.include_router(embeddings.router, prefix="/embeddings", tags=["embeddings"])

def main():
    uvicorn.run(app, host=settings.HOST, port=settings.PORT)

if __name__ == "__main__":
    main()
