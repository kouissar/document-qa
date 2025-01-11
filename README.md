# PDF Question Answering System

A full-stack application that allows users to upload PDF documents and ask questions about their content using AI-powered analysis.

## System Architecture

### Overview

The application consists of two main components:

- Backend: FastAPI-based REST API service
- Frontend: Streamlit web interface

### Technology Stack

- **Backend**

  - FastAPI (REST API framework)
  - LangChain (LLM integration)
  - Groq (LLM provider)
  - ChromaDB (Vector database)
  - PyPDF (PDF processing)
  - HuggingFace Embeddings

- **Frontend**
  - Streamlit
  - Python Requests

## Features

1. **Document Management**

   - PDF file upload
   - Document listing
   - Document deletion
   - PDF download capability

2. **Question Answering**
   - Natural language question processing
   - Context-aware answers
   - Source attribution with page numbers
   - Chunk-based response tracking

## Setup Instructions

### Prerequisites

- Python 3.8+
- Docker (optional)
- Groq API key

### Environment Configuration

1. Create a `.env` file in the backend directory:

env
GROQ_API_KEY=your_groq_api_key
CHROMA_PERSISTENCE_DIR=./chroma_db
MODEL_NAME=mixtral-8x7b-32768
PDF_STORAGE_DIR=./chroma_db/pdfs

### Local Development Setup

1. Backend Setup:

   ```bash
   cd backend
   python -m venv venv
   source venv/bin/activate # On Windows: .\venv\Scripts\activate
   pip install -r requirements.txt
   python run.py
   ```

2. Frontend Setup:
   ```bash
   cd frontend
   python -m venv venv
   source venv/bin/activate # On Windows: .\venv\Scripts\activate
   pip install -r requirements.txt
   streamlit run app.py
   ```

### Docker Setup

```bash
docker-compose up --build
```

## API Documentation

### Endpoints

#### 1. Document Management

##### Upload Document

- **POST** `/upload`
- Accepts PDF files
- Returns processing status

##### List Documents

- **GET** `/documents`
- Returns list of available documents

##### Delete Document

- **DELETE** `/documents/{document_id}`
- Removes document from the system

##### Download Document

- **GET** `/download/{filename}`
- Returns the PDF file

#### 2. Question Answering

##### Ask Question

- **POST** `/ask`
- Request Body:
  ```json
  {
    "question": "string"
  }
  ```
- Response:
  ```json
  {
    "answer": "string",
    "sources": [
      {
        "filename": "string",
        "page": number,
        "chunk": "string",
        "content": "string"
      }
    ]
  }
  ```

### API Docs

http://127.0.0.1:8000/docs

### API Testing

upload a file
`curl -X POST "http://localhost:8000/upload" -F "file=@path/to/your/file.pdf"`

Ask Question
`curl -X POST "http://localhost:8000/ask" -H "Content-Type: application/json" -d '{"question": "Your question here"}'`

List Document
`curl -X GET "http://localhost:8000/documents"`

## Core Components

### Backend Services

1. **Document Service**

   - PDF processing
   - Text extraction
   - Document chunking
   - Vector store management

2. **Embedding Service**

   - Text embedding generation
   - HuggingFace integration

3. **LLM Service**
   - Question processing
   - Context retrieval
   - Answer generation
   - Source attribution

### Frontend Components

1. **Document Management UI**

   - File upload interface
   - Document list
   - Delete functionality

2. **Question Answering UI**
   - Question input
   - Answer display
   - Source display with expandable context
   - PDF download links

## Data Flow

1. **Document Processing**

   - PDF upload → Text extraction → Chunking → Embedding → Vector storage
   - Original PDF storage for download

2. **Question Processing**
   - Question → Embedding → Similarity search → Context retrieval → LLM processing → Answer generation

## Security Considerations

- CORS enabled for development
- File type validation
- Error handling and logging
- Temporary file cleanup
- API error responses

## Limitations

- PDF-only document support
- Dependent on Groq API availability
- Limited by model context window
- Synchronous processing

## Future Improvements

1. Support for additional document formats
2. Batch document processing
3. User authentication
4. Advanced document management features
5. Caching for improved performance
6. Asynchronous document processing
7. Multiple LLM provider support

## Troubleshooting

Common issues and solutions:

1. **PDF Upload Fails**

   - Check file size
   - Verify PDF format
   - Ensure storage directory permissions

2. **Question Answering Issues**

   - Verify Groq API key
   - Check network connectivity
   - Validate vector store status

3. **Performance Issues**
   - Monitor chunk size settings
   - Check available memory
   - Verify database persistence

## Contributing

1. Fork the repository
2. Create a feature branch
3. Commit changes
4. Push to the branch
5. Create a Pull Request

## License

[Add your license information here]
