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
                search_kwargs={"k": 3}  # Retrieve top 3 most relevant chunks
            ),
            question_prompt=question_prompt,
            return_source_documents=True
        )
    
    async def ask_question(self, question: str):
        try:
            result = self.qa_chain({"question": question})
            return {
                "answer": result["answer"],
                "sources": list(set(doc.metadata["source"] for doc in result["source_documents"]))
            }
        except Exception as e:
            print(f"Error in ask_question: {str(e)}")  # Add debugging
            raise e 