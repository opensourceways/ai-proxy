from pydantic import BaseModel

class ChatRequest(BaseModel):
    model: str
    prompt: str
    max_tokens: int
    temperature: int

    def to_dict(self):
        return self.dict()
