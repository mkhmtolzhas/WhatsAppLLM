from openai import AsyncOpenAI
from src.core.config import settings
from src.core.rag.repository import rag_repository
from .schemas import LLMResponse, LLMRequest
from .exeptions import LLMExceptions

class LLMService:
    def __init__(self, openai_api_key: str = settings.openai_api_key):
        self.client = AsyncOpenAI(api_key=openai_api_key)
        self.system_message = "The following is a conversation with an AI assistant. The assistant is helpful, creative, clever, and very friendly. The assistant helps with tasks like scheduling, generating text, and answering questions."
    
    async def get_response(self, message: LLMRequest) -> LLMResponse:
        if not message:
            raise LLMExceptions.BadRequest()
        
        context = await rag_repository.search_embeddings(message.message, message.user)
        
        await rag_repository.upsert_embeddings(message.message, message.user)

        try:
            response = await self.client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": self.system_message},
                    {"role": "user", "content": f": Context :{context}\n\nMessage: {message.message}"},
                ],
            )
            
            if not response or not response.choices or not response.choices[0].message:
                pass 

            return LLMResponse(response=response.choices[0].message.content, user=message.user)
        except Exception as e:
            raise LLMExceptions.InternalServerError()


llm_service = LLMService()