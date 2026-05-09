import streamlit as st
# New stable import paths
from langchain_ollama import OllamaLLM 
from langchain_core.prompts import PromptTemplate
from langchain_text_splitters import RecursiveCharacterTextSplitter
import spacy

# Load SpaCy
try:
    nlp = spacy.load("en_core_web_md")
except Exception:
    st.error("Missing SpaCy model. Run: python -m spacy download en_core_web_md")

st.title("RAG: Long Story Assistant")

long_text = st.text_area(label="Paste your long text here.", height=300)
question = st.text_input(label="Enter your question:")
button = st.button("Answer")

if button:
    if long_text and question:
        # Initialize Ollama
        llm = OllamaLLM(model='llama3.1:8b')

        # Modern Template approach
        template = """Answer the question based only on the context below.
        
        Context: {context}
        
        Question: {question}
        """
        prompt = PromptTemplate.from_template(template)

        # 1. Chunking - Using the updated splitter path
        text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=150)
        chunks = text_splitter.create_documents([long_text])

        # 2. Semantic Search
        similarities = []
        query_doc = nlp(question)
        for chunk in chunks:
            score = query_doc.similarity(nlp(chunk.page_content))
            similarities.append((score, chunk.page_content))

        # 3. Retrieval (Top 3)
        relevant_chunks = sorted(similarities, key=lambda x: x[0], reverse=True)[:3]
        context_block = "\n\n".join([c[1] for c in relevant_chunks])

        # 4. Generation using LCEL (Modern LangChain syntax)
        chain = prompt | llm
        response = chain.invoke({"context": context_block, "question": question})

        st.subheader("Answer:")
        st.write(response)
    else:
        st.warning("Please fill in both fields.")