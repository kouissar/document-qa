from langchain_community.vectorstores import Chroma
from .embedding_service import EmbeddingService
from .document_service import DocumentService
from .llm_service import LLMService
from ..config import settings
import os

# Ensure the ChromaDB directory exists
os.makedirs(settings.CHROMA_PERSISTENCE_DIR, exist_ok=True)

# Initialize services
embedding_service = EmbeddingService()

# Create LangChain's Chroma vector store
vector_store = Chroma(
    persist_directory=settings.CHROMA_PERSISTENCE_DIR,
    embedding_function=embedding_service._embeddings,
    collection_name="pdf_collection"
)

document_service = DocumentService(embedding_service, vector_store)
llm_service = LLMService(vector_store) 