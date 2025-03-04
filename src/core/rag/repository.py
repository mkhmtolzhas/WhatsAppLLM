from asyncio import to_thread
from openai import AsyncOpenAI
from pinecone.grpc import PineconeGRPC as Pinecone
from src.core.config import settings
from .utils import RAGUtils
from .exceptions import RAGExceptions
from datetime import datetime
from src.core.cache.client import cache_client
from json import loads, dumps


class RAGRepository:
    def __init__(self, openai_api_key: str = settings.openai_api_key, pinecone_api_key: str = settings.pinecone_api_key, index_name: str = settings.pinecone_index_name):
        self.openai = AsyncOpenAI(api_key=openai_api_key)
        self.pinecone = Pinecone(api_key=pinecone_api_key)
        self.index= self.pinecone.Index(name=index_name)
    
    
    async def get_embeddings(self, text: str):
        try:
            cached_embedding = await cache_client.get(text)
            if cached_embedding:
                return loads(cached_embedding)
            
            response = await self.openai.embeddings.create(
                input=text,
                model="text-embedding-3-small"
            )

            embedding = response.data[0].embedding
            await cache_client.set(text, dumps(embedding), expire=86400)

            return response.data[0].embedding
        except Exception as e:
            raise RAGExceptions.FailedToGetEmbeddings()
            
    
    async def upsert_embeddings(self, text: str, user: str):
        try:
            cache_key = f"upsert:{user}:{RAGUtils.get_hash(text)}"
            cached_result = await cache_client.get(cache_key)

            if cached_result:
                return loads(cached_result)

            embedding = await self.get_embeddings(text)
            if not embedding:
                raise RAGExceptions.EmbeddingsNotFound()

            vectors = [{
                "values": embedding,
                "id": RAGUtils.get_hash(text),
                "metadata": {
                    "message": text,
                    "timestamp": datetime.utcnow().isoformat()
                }
            }]

            await to_thread(
                self.index.upsert,
                vectors=vectors, 
                namespace=f"ctx_{user}"
            )

            result = {"message": "Embeddings upserted successfully"}

            await cache_client.set(cache_key, dumps(result), expire=86400)
            return result
        except Exception as e:
            raise RAGExceptions.EmbeddingsUpsertFailed(detail=str(e))
    

    async def search_embeddings(self, text: str, user: str):
        try:
            cache_key = f"search:{user}:{RAGUtils.get_hash(text)}"
            cached_result = await cache_client.get(cache_key)

            if cached_result is not None:
                return loads(cached_result)

            embedding = await self.get_embeddings(text)
            if not embedding:
                raise RAGExceptions.EmbeddingsNotFound()

            result = await to_thread(
                self.index.query,
                vector=embedding,
                top_k=6,
                namespace=f"ctx_{user}",
                include_metadata=True
            )

            formatted_result = {
                "messages": [
                    {
                        "id": r["id"],
                        "score": r["score"],
                        "metadata": r["metadata"]
                    }
                    for r in result["matches"]
                ]
            }

            await cache_client.set(cache_key, dumps(formatted_result), expire=3600)
            return formatted_result
        except Exception as e:
            raise RAGExceptions.EmbeddingsSearchFailed(detail=str(e))
        


rag_repository = RAGRepository()