import streamlit as st
import requests
import json

BACKEND_URL = "http://localhost:8000"

st.title("PDF Question Answering System")

# File upload section
st.header("Upload PDF")
uploaded_file = st.file_uploader("Choose a PDF file", type="pdf", key="pdf_uploader")
if uploaded_file is not None:
    if st.button("Upload PDF"):  # Add explicit upload button
        files = {"file": uploaded_file}
        response = requests.post(f"{BACKEND_URL}/upload", files=files)
        if response.status_code == 200:
            st.success("File uploaded successfully!")
            # Clear the file uploader
            st.session_state["pdf_uploader"] = None
            # Refresh the page once
            st.experimental_rerun()

# Document list section
st.header("Available Documents")
if st.button("Refresh Documents"):
    try:
        response = requests.get(f"{BACKEND_URL}/documents")
        if response.status_code == 200:
            documents = response.json().get("documents", [])
            if documents:
                for doc in documents:
                    col1, col2 = st.columns([3, 1])
                    with col1:
                        st.write(doc)
                    with col2:
                        if st.button("Delete", key=f"delete_{doc}"):
                            delete_response = requests.delete(f"{BACKEND_URL}/documents/{doc}")
                            if delete_response.status_code == 200:
                                st.success(f"Deleted {doc}")
                                st.experimental_rerun()
            else:
                st.info("No documents found in the database.")
        else:
            st.error("Failed to fetch documents")
    except Exception as e:
        st.error(f"Error: {str(e)}")

# Question answering section
st.header("Ask a Question")
question = st.text_input("Enter your question:")
if st.button("Ask"):
    if question:
        try:
            response = requests.post(
                f"{BACKEND_URL}/ask",
                json={"question": question}
            )
            if response.status_code == 200:
                result = response.json()
                st.write("Answer:", result["answer"])
                if result["sources"]:
                    st.write("Sources:", ", ".join(result["sources"]))
            else:
                st.error("Failed to get answer")
        except Exception as e:
            st.error(f"Error: {str(e)}")
    else:
        st.warning("Please enter a question") 