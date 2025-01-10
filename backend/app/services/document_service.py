from typing import List
import os
from pypdf import PdfReader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.schema import Document

class DocumentService:
    def __init__(self, embedding_service, vector_store):
        self.embedding_service = embedding_service
        self.vector_store = vector_store
        self.text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=1000,
            chunk_overlap=200
        )
    
    async def process_pdf(self, file_path: str, original_filename: str) -> List[Document]:
        try:
            # Check if document already exists
            collection = self.vector_store._collection
            if collection:
                result = collection.get()
                if result and result['metadatas']:
                    existing_sources = {meta['source'] for meta in result['metadatas'] if meta and 'source' in meta}
                    if original_filename in existing_sources:
                        print(f"Document {original_filename} already exists")
                        return []

            # Extract text from PDF
            pdf_reader = PdfReader(file_path)
            text = ""
            for page in pdf_reader.pages:
                text += page.extract_text()
            
            print(f"Extracted {len(text)} characters from PDF")
            
            # Split text into chunks
            texts = self.text_splitter.split_text(text)
            print(f"Split into {len(texts)} chunks")
            
            # Create documents with original filename
            documents = [
                Document(
                    page_content=t,
                    metadata={"source": original_filename}
                ) for t in texts
            ]
            
            # Add to vector store
            self.vector_store.add_documents(documents)
            self.vector_store.persist()
            
            # Verify documents were added
            if collection:
                result = collection.get()
                print(f"Vector store now contains {len(result['metadatas'])} documents")
            
            return documents
        except Exception as e:
            print(f"Error processing PDF: {str(e)}")
            raise e 