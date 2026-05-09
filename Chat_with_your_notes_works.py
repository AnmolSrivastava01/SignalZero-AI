import streamlit as st
# New stable import paths for LangChain 0.2+
from langchain_ollama import OllamaLLM 
from langchain_core.prompts import PromptTemplate
from langchain_text_splitters import RecursiveCharacterTextSplitter
import spacy
import os

# --- INITIALIZATION ---
# Load SpaCy for embedding calculations
try:
    nlp = spacy.load("en_core_web_md")
except Exception:
    st.error("Missing SpaCy model. Run: python -m spacy download en_core_web_md")

# Ensure the persistence file exists
if not os.path.exists("note.text"):
    with open("note.text", "w") as f:
        f.write("")

st.title("🗒️ Chat with Your Note")

# --- Part 1: Adding New Notes ---
with st.form(key='note_form', clear_on_submit=True):
    note = st.text_area(label="Paste your note here to save it forever.", height=200)
    submit_button = st.form_submit_button(label='Save Note')

if submit_button and note:
    # Open in read mode to check content
    with open("note.text", 'r') as file:
        content = file.read()
    
    # Simple deduplication
    if note not in content:
        # Append mode 'a' is safer and more efficient than overwriting with 'w'
        with open("note.text", 'a') as file:
            file.write(f"\n\n{note}")
        st.success("Note saved successfully!")
    else:
        st.warning("This note already exists in your knowledge base.")

# --- Part 2: Q&A Interface ---
st.divider()
question = st.text_input(label="Ask a question about your saved notes:")
button = st.button("ASK AI")

if button and question:
    with st.spinner("Searching your notes..."):
        # Initialize the modern local LLM class
        llm = OllamaLLM(model='llama3.1:8b')

        # Define the modern RAG prompt template
        template = """You are a helpful knowledge assistant. Use the provided notes to answer the question.
        
        Question: {question}
        
        Notes Content:
        {context}
        """
        prompt = PromptTemplate.from_template(template)

        # Load the accumulated notes
        with open("note.text", 'r') as file:
            full_content = file.read()
            
        if not full_content.strip():
            st.error("Your note file is empty! Please save some notes first.")
        else:
            # 1. Chunking
            text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=150)
            chunks = text_splitter.create_documents([full_content])

            # 2. Semantic Search using SpaCy
            similarities = []
            query_doc = nlp(question)
            for chunk in chunks:
                score = query_doc.similarity(nlp(chunk.page_content))
                similarities.append((score, chunk.page_content))

            # 3. Filtering (Top 3 matches)
            ordered_chunks = sorted(similarities, key=lambda x: x[0], reverse=True)[:3]

            context_block = ""
            for score, text in ordered_chunks:
                # Optional: UI feedback on what was found
                st.caption(f"Relevance Score: {score:.4f}")
                context_block += f"{text}\n\n"
            
            # 4. Generation using the modern Pipe syntax
            chain = prompt | llm
            answer = chain.invoke({"context": context_block, "question": question})

            st.subheader("Answer:")
            st.write(answer)