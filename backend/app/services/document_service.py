from typing import List
import os
from pypdf import PdfReader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.schema import Document
from app.config import settings

class DocumentService:
    def __init__(self, embedding_service, vector_store):
        self.embedding_service = embedding_service
        self.vector_store = vector_store
        self.text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=1000,
            chunk_overlap=200
        )
        # Ensure PDF storage directory exists
        os.makedirs(settings.PDF_STORAGE_DIR, exist_ok=True)
    
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

            # Extract text from PDF with page numbers
            pdf_reader = PdfReader(file_path)
            text_by_page = []
            for page_num, page in enumerate(pdf_reader.pages, 1):
                text_by_page.append((page_num, page.extract_text()))
            
            print(f"Extracted text from {len(text_by_page)} pages")
            
            documents = []
            for page_num, text in text_by_page:
                # Split text into chunks for each page
                chunks = self.text_splitter.split_text(text)
                # Create documents with page metadata
                page_docs = [
                    Document(
                        page_content=chunk,
                        metadata={
                            "source": original_filename,
                            "page": page_num,
                            "chunk": i + 1,
                            "total_chunks": len(chunks)
                        }
                    ) for i, chunk in enumerate(chunks)
                ]
                documents.extend(page_docs)
            
            # Save original PDF to storage
            pdf_path = os.path.join(settings.PDF_STORAGE_DIR, original_filename)
            with open(file_path, 'rb') as src, open(pdf_path, 'wb') as dst:
                dst.write(src.read())
            
            # Add to vector store
            self.vector_store.add_documents(documents)
            self.vector_store.persist()
            
            return documents
        except Exception as e:
            print(f"Error processing PDF: {str(e)}")
            raise e 