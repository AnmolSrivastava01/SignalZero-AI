import streamlit as st
from langchain_ollama import OllamaLLM
from langchain_core.prompts import PromptTemplate
import spacy
from datetime import datetime
import json
import os

# --- INITIALIZATION ---
# Load SpaCy for semantic search
try:
    nlp = spacy.load("en_core_web_md")
except:
    st.error("Missing SpaCy model. Run: python -m spacy download en_core_web_md")

# Ensure diary.json exists to avoid crash on load
if not os.path.exists("diary.json"):
    with open("diary.json", "w") as f:
        json.dump({}, f)

st.title("📔 Chat with Your Diary")

# --- UI: Date & Note Input ---
today = datetime.now().date()
selected_date = st.date_input("Select a date", value=today)

with st.form(key='diary_form', clear_on_submit=True):
    note = st.text_area(label="Write your diary entry here...", height=200)
    submit_button = st.form_submit_button(label='Save Entry')

if submit_button and note:
    date_str = str(selected_date)
    
    # Load and Update
    with open("diary.json", 'r') as f:
        data = json.load(f)
    
    if date_str in data:
        if note not in data[date_str]:
            data[date_str] += f"\n\n{note}"
    else:
        data[date_str] = note
        
    with open("diary.json", 'w') as f:
        json.dump(data, f, indent=4)
    st.success(f"Saved to {date_str}!")

# --- Q&A Section ---
st.divider()
question = st.text_input(label="Ask a question about your past entries:")
button = st.button("Search Diary")

if button and question:
    with st.spinner("Searching your memories..."):
        # Initialize Modern LLM
        llm = OllamaLLM(model='llama3.1:8b')

        template = """You are a personal diary assistant. Use the following diary entries to answer the user.
        If the answer isn't in the diary, say you don't know.

        Question: {question}

        Diary Entries:
        {context}
        """
        prompt = PromptTemplate.from_template(template)

        # Load diary
        with open("diary.json", 'r') as f:
            data = json.load(f)
            
        if not data:
            st.warning("Your diary is empty!")
        else:
            # Semantic Search
            similarities = []
            query_vec = nlp(question)
            
            for date, content in data.items():
                score = query_vec.similarity(nlp(content))
                similarities.append((score, f"Date: {date}\nEntry: {content}"))

            # Top 3 relevant days
            ordered_results = sorted(similarities, key=lambda x: x[0], reverse=True)[:3]

            context_text = ""
            for score, entry in ordered_results:
                if score > 0.3: # Only show somewhat relevant matches
                    st.caption(f"Relevance: {score:.2f}")
                    st.info(entry)
                    context_text += f"{entry}\n\n"
            
            # Generate Answer (Modern LCEL Pipe)
            chain = prompt | llm
            answer = chain.invoke({"context": context_text, "question": question})

            st.subheader("AI Response:")
            st.write(answer)