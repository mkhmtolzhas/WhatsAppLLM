from hashlib import md5

class RAGUtils:
    @staticmethod
    def get_hash(text: str) -> str:
        return md5(text.encode()).hexdigest()
    