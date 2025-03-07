from langchain_groq import ChatGroq
from langchain.chains import RetrievalQAWithSourcesChain
from langchain.prompts import PromptTemplate
from app.config import settings

class LLMService:
    def __init__(self, vector_store):
        self.llm = ChatGroq(
            api_key=settings.GROQ_API_KEY,
            model_name=settings.MODEL_NAME
        )
        self.vector_store = vector_store
        
        # Define the question prompt
        question_prompt = PromptTemplate(
            template="""Use the following pieces of context to answer the question at the end. If you don't know the answer, just say that you don't know, don't try to make up an answer.

Context:
{context}

Question: {question}

Answer the question using only the provided context. If you cannot answer this question based on the context, say "I cannot answer this question based on the provided context."

Answer:""",
            input_variables=["context", "question"]
        )
        
        self.qa_chain = RetrievalQAWithSourcesChain.from_llm(
            llm=self.llm,
            retriever=self.vector_store.as_retriever(
                search_kwargs={"k": 2}  # Retrieve top 3 most relevant chunks
            ),
            question_prompt=question_prompt,
            return_source_documents=True
        )
    
    async def ask_question(self, question: str):
        try:
            result = self.qa_chain({"question": question})
            sources = []
            for doc in result["source_documents"]:
                metadata = doc.metadata
                source_info = {
                    "filename": metadata.get("source", "Unknown"),
                    "page": metadata.get("page", 1),
                    "content": doc.page_content  # Include the chunk content
                }
                # Only add chunk info if available
                if "chunk" in metadata and "total_chunks" in metadata:
                    source_info["chunk"] = f"{metadata['chunk']}/{metadata['total_chunks']}"
                else:
                    source_info["chunk"] = "1/1"
                
                # Only add unique sources
                if source_info not in sources:
                    sources.append(source_info)
            
            return {
                "answer": result["answer"],
                "sources": sources
            }
        except Exception as e:
            print(f"Error in ask_question: {str(e)}")
            print(f"Result structure: {result.keys() if 'result' in locals() else 'No result'}")
            if 'result' in locals() and "source_documents" in result:
                print(f"Source docs metadata: {[doc.metadata for doc in result['source_documents']]}")
            raise e 