from pydantic import BaseModel

class LLMBase(BaseModel):
    user: str
    
    class Config:
        from_attributes = True

class LLMRequest(LLMBase):
    message: str

class LLMResponse(LLMBase):
    response: str