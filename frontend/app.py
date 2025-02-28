import streamlit as st
import requests
import json

BACKEND_URL = "http://localhost:8000"

# Custom CSS for styling
st.markdown(
    """
    <style>
    body {
        background-color: #f0f4f8;
        color: #333;
    }
    .title {
        font-size: 2.5em;
        color: #4a90e2;
        text-align: center;
        margin-bottom: 20px;
    }
    .header {
        color: #d35400;
        font-size: 1.5em;
        margin-top: 20px;
    }
    .subheader {
        color: #2980b9;
        font-size: 1.2em;
        margin-top: 15px;
    }
    .button {
        background-color: #4CAF50; /* Green */
        color: white;
        padding: 10px 20px;
        border: none;
        border-radius: 5px;
        cursor: pointer;
    }
    .button:hover {
        background-color: #45a049;
    }
    .info {
        background-color: #e7f3fe;
        color: #31708f;
        padding: 10px;
        border: 1px solid #bce8f1;
        border-radius: 5px;
    }
    </style>
    """,
    unsafe_allow_html=True
)

st.markdown('<h1 class="title">Infinite OSHO</h1>', unsafe_allow_html=True)
st.markdown('<h2 class="header">Heart to Heart Talk With OSHO</h2>', unsafe_allow_html=True)

# File upload section
# st.subheader("Upload PDF")
uploaded_file = st.file_uploader("Choose a PDF file", type="pdf", key="pdf_uploader")
if uploaded_file is not None:
    if st.markdown('<button class="button" style="background-color: #4CAF50; color: white; padding: 10px 20px; border: none; border-radius: 5px; cursor: pointer;">Upload PDF</button>', unsafe_allow_html=True):
        files = {"file": uploaded_file}
        response = requests.post(f"{BACKEND_URL}/upload", files=files)
        if response.status_code == 200:
            st.success("File uploaded successfully!")
            # Clear the file uploader
            st.session_state["pdf_uploader"] = None
            # Refresh the page once
            st.experimental_rerun()

# Document list section
st.markdown('<h3 class="subheader">Available Documents</h3>', unsafe_allow_html=True)
if st.markdown('<button class="button" style="background-color: #4CAF50; color: white; padding: 10px 20px; border: none; border-radius: 5px; cursor: pointer;">Refresh Documents</button>', unsafe_allow_html=True):
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
# st.subheader("Ask a Question")
st.markdown('<h3 class="subheader">Ask a Question</h3>', unsafe_allow_html=True)
question = st.text_input("Enter your question:")
if st.markdown('<button class="button" style="background-color: #4CAF50; color: white; padding: 10px 20px; border: none; border-radius: 5px; cursor: pointer;">Ask</button>', unsafe_allow_html=True):
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
                    st.write("Sources:")
                    for i, source in enumerate(result["sources"]):
                        # Create an expander for each source
                        with st.expander(
                            f"📄 {source['filename']} (Page {source['page']}, Chunk {source['chunk']})"
                        ):
                            # Show the chunk content
                            if "content" in source:
                                st.text_area(
                                    "Relevant Text:",
                                    source["content"],
                                    height=100,
                                    disabled=True
                                )
                            # Add download button inside expander
                            download_url = f"{BACKEND_URL}/download/{source['filename']}"
                            st.markdown(f"[Download PDF]({download_url})")
            else:
                st.error("Failed to get answer")
        except Exception as e:
            st.error(f"Error: {str(e)}")
    else:
        st.warning("Please enter a question")
        
# sentiment_mapping = [":material/thumb_down:", ":material/thumb_up:"]
# selected = st.sidebar.feedback("thumbs")
# if selected is not None:
#     st.sidebar.markdown(f"You selected: {sentiment_mapping[selected]}") 