from langchain.embeddings import HuggingFaceEmbeddings
from typing import List

class EmbeddingService:
    def __init__(self):
        self._embeddings = HuggingFaceEmbeddings()
    
    def __call__(self, input: List[str]) -> List[List[float]]:
        """
        Generate embeddings for a list of texts.
        Args:
            input: List of texts to generate embeddings for
        Returns:
            List of embeddings (each embedding is a list of floats)
        """
        return self._embeddings.embed_documents(input) 