from pydantic import BaseModel

class LLMBase(BaseModel):
    user: str
    pass

class LLMRequest(LLMBase):
    message: str

class LLMResponse(LLMBase):
    response: str