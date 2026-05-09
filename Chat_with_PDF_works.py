import streamlit as st
import ollama
import fitz  # PyMuPDF
import os

# --- PAGE CONFIG ---
st.set_page_config(page_title="Local PDF Chat", layout="centered")
st.title("📄 Chat with PDF (Local LLM)")

# --- UTILITY FUNCTIONS ---

def extract_text_from_pdf(uploaded_file):
    """Extracts text from a PDF file object in memory."""
    try:
        # Read the file into a byte stream
        file_bytes = uploaded_file.read()
        # Open PDF from memory stream
        doc = fitz.open(stream=file_bytes, filetype="pdf")
        
        text = ""
        for page in doc:
            text += page.get_text()
        
        doc.close()
        return text
    except Exception as e:
        st.error(f"Error reading PDF: {e}")
        return None

# --- UI LAYOUT ---

uploaded_file = st.file_uploader("Upload your PDF file", type="pdf")

if uploaded_file is not None:
    # Extract text immediately without saving to disk
    with st.spinner("Extracting text from PDF..."):
        pdf_text = extract_text_from_pdf(uploaded_file)

    if pdf_text:
        st.success("PDF loaded successfully!")
        
        # User Input
        prompt = st.text_area("Ask a question about this document:")
        
        if st.button("Generate Answer"):
            if prompt:
                with st.spinner("Thinking..."):
                    try:
                        # Constructing the RAG prompt
                        combined_prompt = (
                            f"Context extracted from PDF:\n{pdf_text[:10000]}\n\n"
                            f"User Question: {prompt}\n\n"
                            f"Answer based strictly on the context provided above."
                        )
                        
                        # Generate response using Ollama
                        # Ensure 'llama3.1:8b' is pulled: 'ollama pull llama3.1:8b'
                        response = ollama.generate(model='llama3.1:8b', prompt=combined_prompt)
                        
                        st.subheader("Response:")
                        st.markdown(response["response"])
                        
                    except Exception as e:
                        st.error(f"Ollama Error: {e}")
            else:
                st.warning("Please enter a question first.")
    else:
        st.error("Could not extract text from the PDF. Is the file password protected?")

else:
    st.info("Please upload a PDF to get started.")

# Optional footer to check directory
st.sidebar.markdown(f"**Current Directory:** `{os.getcwd()}`")