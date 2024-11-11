from pydantic import BaseModel

class EmbeddingsRequest(BaseModel):
    prompt: str
    model: str
    encoding_format: str

    def to_dict(self):
        return self.dict()