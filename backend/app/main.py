from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Optional
import os
import tempfile
from app.services import document_service, llm_service
from fastapi.responses import FileResponse

app = FastAPI()

# Enable CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class QuestionRequest(BaseModel):
    question: str
    
class QuestionResponse(BaseModel):
    answer: str
    sources: List[dict]

@app.post("/upload")
async def upload_document(file: UploadFile = File(...)):
    if not file.filename.endswith('.pdf'):
        raise HTTPException(status_code=400, detail="Only PDF files are allowed")
    
    # Save the uploaded file temporarily
    with tempfile.NamedTemporaryFile(delete=False, suffix='.pdf') as tmp_file:
        content = await file.read()
        tmp_file.write(content)
        tmp_file_path = tmp_file.name
    
    try:
        # Process the PDF file with original filename
        documents = await document_service.process_pdf(tmp_file_path, file.filename)
        if not documents:  # If empty list returned, file already exists
            return {"message": "File already exists in the database"}
        return {"message": f"File uploaded successfully. Processed {len(documents)} chunks."}
    finally:
        # Clean up the temporary file
        os.unlink(tmp_file_path)

@app.post("/ask", response_model=QuestionResponse)
async def ask_question(request: QuestionRequest):
    try:
        response = await llm_service.ask_question(request.question)
        return response
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/documents")
async def list_documents():
    try:
        # Get all documents from the collection
        collection = document_service.vector_store._collection
        if collection is None:
            return {"documents": []}
            
        # Get all documents metadata
        result = collection.get()
        if not result or not result['metadatas']:
            return {"documents": []}
            
        # Extract unique source files from metadata
        sources = set()
        for metadata in result['metadatas']:
            if metadata and 'source' in metadata:
                sources.add(metadata['source'])
                
        return {"documents": list(sources)}
    except Exception as e:
        print(f"Error listing documents: {str(e)}")  # Debug log
        raise HTTPException(status_code=500, detail=str(e))

@app.delete("/documents/{document_id}")
async def delete_document(document_id: str):
    try:
        # Delete documents with matching source
        document_service.vector_store.delete({"source": document_id})
        document_service.vector_store.persist()  # Save changes to disk
        return {"message": "Document deleted successfully"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e)) 

@app.get("/download/{filename}")
async def download_file(filename: str):
    file_path = os.path.join(settings.PDF_STORAGE_DIR, filename)
    if not os.path.exists(file_path):
        print(f"File not found: {file_path}")  # Add debug logging
        raise HTTPException(status_code=404, detail="File not found")
    try:
        return FileResponse(
            file_path,
            media_type="application/pdf",
            filename=filename
        )
    except Exception as e:
        print(f"Error serving file: {str(e)}")  # Add debug logging
        raise HTTPException(status_code=500, detail=str(e)) 