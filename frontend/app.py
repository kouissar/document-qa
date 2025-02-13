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
                # Feedback section
                feedback = st.text_area("Provide your feedback on the answer:")
                if st.button("Submit Feedback"):
                    feedback_data = {
                        "question": question,
                        "response": result["answer"],
                        "feedback": feedback
                    }
                    print("Feedback data being sent:", feedback_data)  # Debug log
                    feedback_response = requests.post(
                        f"{BACKEND_URL}/feedback",
                        json=feedback_data
                    )
                    if feedback_response.status_code == 200:
                        st.success("Feedback submitted successfully!")
                    else:
                        st.error("Failed to submit feedback")
                        st.write(feedback_response.text)  # Log the response for debugging
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

# Feedback review section
st.header("Review Feedback")
if st.button("Load Feedback"):
    try:
        response = requests.get(f"{BACKEND_URL}/feedback")
        if response.status_code == 200:
            feedback_list = response.json().get("feedback", [])
            if feedback_list:
                for feedback in feedback_list:
                    question, response_text, user_feedback = feedback
                    st.subheader("Question:")
                    st.write(question)
                    st.subheader("Response:")
                    st.write(response_text)
                    st.subheader("User Feedback:")
                    st.write(user_feedback)
                    st.markdown("---")  # Separator between feedback entries
            else:
                st.info("No feedback found.")
        else:
            st.error("Failed to load feedback.")
    except Exception as e:
        st.error(f"Error: {str(e)}") 