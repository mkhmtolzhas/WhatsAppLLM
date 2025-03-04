from fastapi import HTTPException

class RAGExceptions:
    class InvalidInput(HTTPException):
        def __init__(self):
            super().__init__(status_code=400, detail="Invalid input")
    
    class EmbeddingsNotFound(HTTPException):
        def __init__(self):
            super().__init__(status_code=404, detail="Embeddings not found")

    class EmbeddingsUpsertFailed(HTTPException):
        def __init__(self, detail: str = "Embeddings upsert failed"):
            super().__init__(status_code=500, detail=detail)
        
    class EmbeddingsSearchFailed(HTTPException):
        def __init__(self, detail: str = "Embeddings search failed"):
            super().__init__(status_code=500, detail=detail)

    class FailedToGetEmbeddings(HTTPException):
        def __init__(self):
            super().__init__(status_code=500, detail="Failed to get embeddings")
        

    