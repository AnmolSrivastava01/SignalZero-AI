# # import streamlit as st
# # import ollama
# # import fitz  # PyMuPDF
# # import os
# # import json
# # import tempfile
# # import spacy
# # import sys
# # import io
# # from datetime import datetime
# # from langchain_ollama import OllamaLLM 
# # from langchain_core.prompts import PromptTemplate
# # from langchain_text_splitters import RecursiveCharacterTextSplitter
# # import whisper
# # from pydub import AudioSegment

# # # ─── 1. SYSTEM & COMPATIBILITY CONFIG ─────────────────────────────────────────
# # ffmpeg_folder = r'C:\ffmpeg\bin' #
# # os.environ["PATH"] += os.pathsep + ffmpeg_folder
# # AudioSegment.converter = os.path.join(ffmpeg_folder, "ffmpeg.exe")
# # AudioSegment.ffprobe   = os.path.join(ffmpeg_folder, "ffprobe.exe")

# # try:
# #     import audioop
# # except ImportError:
# #     try:
# #         import audioop_lts as audioop
# #         sys.modules["audioop"] = audioop
# #     except ImportError:
# #         pass # Streamlit handles specific errors in the UI

# # # ─── 2. GLOBAL SETTINGS & STYLING ─────────────────────────────────────────────
# # st.set_page_config(page_title="SignalZero", page_icon="⚡", layout="wide")

# # st.markdown("""
# # <style>
# #     @import url('https://fonts.googleapis.com/css2?family=Space+Mono&family=Syne:wght@700&display=swap');
# #     :root { --accent: #00c8ff; --bg: #080d1a; }
# #     .stApp { background-color: var(--bg); color: #e8edf5; }
# #     .stButton>button { border: 1px solid var(--accent); color: var(--accent); background: transparent; font-family: 'Space Mono'; }
# #     .answer-box { background: #0d1526; border-left: 3px solid var(--accent); padding: 15px; border-radius: 5px; font-family: 'Space Mono'; }
# # </style>
# # """, unsafe_allow_html=True)

# # # ─── 3. SHARED RESOURCE LOADING ───────────────────────────────────────────────
# # @st.cache_resource
# # def get_models():
# #     nlp = spacy.load("en_core_web_md") #
# #     whisper_model = whisper.load_model("base") #
# #     llm = OllamaLLM(model='llama3.1:8b') #
# #     return nlp, whisper_model, llm

# # nlp, whisper_model, llm = get_models()

# # # ─── 4. SIDEBAR NAVIGATION ──────────────────────────────────────────────────
# # with st.sidebar:
# #     st.title("⚡ SignalZero")
# #     mode = st.radio("SELECT MODULE", [
# #         "🏠 Home", "📄 PDF Chat", "🎥 Video Chat", "🖼️ Image Describer", 
# #         "🐍 Code Tutor", "🗒️ Note Keeper", "📔 Diary Chat", "📖 Story RAG"
# #     ])
# #     st.divider()
# #     st.info("Local AI Mode: Active")

# # # ─── 5. MODULE LOGIC ─────────────────────────────────────────────────────────

# # if mode == "🏠 Home":
# #     st.header("Welcome to SignalZero")
# #     st.write("A fully offline, local AI workstation powered by Ollama, Llama 3.1, and Whisper.")

# # elif mode == "📄 PDF Chat":
# #     st.subheader("📄 Chat with your PDF")
# #     up_pdf = st.file_uploader("Upload PDF", type="pdf")
# #     if up_pdf:
# #         doc = fitz.open(stream=up_pdf.read(), filetype="pdf")
# #         text = "".join([p.get_text() for p in doc]) #
# #         q = st.text_input("Ask about the PDF")
# #         if st.button("Query PDF"):
# #             res = ollama.generate(model='llama3.1:8b', prompt=f"Context: {text[:8000]}\nQuestion: {q}") #
# #             st.markdown(f"<div class='answer-box'>{res['response']}</div>", unsafe_allow_html=True)

# # elif mode == "🎥 Video Chat":
# #     st.subheader("🎥 Video AI Assistant")
# #     up_vid = st.file_uploader("Upload MP4", type=["mp4"]) #
# #     if up_vid:
# #         with tempfile.NamedTemporaryFile(delete=False, suffix=".mp4") as t:
# #             t.write(up_vid.read())
# #             v_path = t.name
# #         a_path = v_path.replace(".mp4", ".wav")
# #         if 'v_transcript' not in st.session_state:
# #             AudioSegment.from_file(v_path).export(a_path, format="wav") #
# #             st.session_state.v_transcript = whisper_model.transcribe(a_path)['text'] #
# #         st.write(st.session_state.v_transcript)
# #         q = st.text_input("Ask about the video")
# #         if st.button("Ask Video AI"):
# #             res = ollama.generate(model='llama3.1:8b', prompt=f"Context: {st.session_state.v_transcript}\nQuestion: {q}")
# #             st.write(res['response'])

# # elif mode == "🖼️ Image Describer":
# #     st.subheader("🖼️ Vision AI")
# #     up_img = st.file_uploader("Upload Image", type=["jpg", "png"]) #
# #     if up_img:
# #         st.image(up_img)
# #         if st.button("Describe Image"):
# #             res = ollama.chat(model='llava:7b', messages=[{'role':'user','content':'Describe this','images':[up_img.getvalue()]}]) #
# #             st.markdown(f"<div class='answer-box'>{res['message']['content']}</div>", unsafe_allow_html=True)

# # elif mode == "🐍 Code Tutor":
# #     st.subheader("🐍 Self-Fixing Code Tutor")
# #     p = st.text_area("What should I code?") #
# #     if st.button("Generate & Run"):
# #         res = ollama.generate(model='llama3.1:8b', prompt=f"{p}\nOutput ONLY Python code.") #
# #         code = res['response'].replace("```python", "").replace("```", "").strip()
# #         st.code(code)
# #         try:
# #             exec(code) #
# #             st.success("Execution Successful")
# #         except Exception as e:
# #             st.error(f"Error: {e}")

# # elif mode == "🗒️ Note Keeper":
# #     st.subheader("🗒️ Personal Knowledge Base")
# #     with st.form("note_form"):
# #         note = st.text_area("New Note") #
# #         if st.form_submit_button("Save"):
# #             with open("note.text", "a") as f: f.write(f"\n\n{note}")
# #             st.success("Saved")
# #     q = st.text_input("Search Notes")
# #     if st.button("Ask Notes") and os.path.exists("note.text"):
# #         with open("note.text", "r") as f: context = f.read()
# #         res = llm.invoke(f"Context: {context}\nQuestion: {q}") #
# #         st.write(res)

# # elif mode == "📔 Diary Chat":
# #     st.subheader("📔 Memory Retrieval")
# #     d_date = st.date_input("Date") #
# #     d_note = st.text_area("Write Entry")
# #     if st.button("Save Diary"):
# #         data = json.load(open("diary.json")) if os.path.exists("diary.json") else {}
# #         data[str(d_date)] = d_note
# #         json.dump(data, open("diary.json", "w")) #
# #     q = st.text_input("Search Memories")
# #     if st.button("Recall"):
# #         data = json.load(open("diary.json"))
# #         # Simplified semantic retrieval
# #         matches = [v for k,v in data.items() if nlp(q).similarity(nlp(v)) > 0.4]
# #         res = llm.invoke(f"Context: {' '.join(matches)}\nQuestion: {q}")
# #         st.write(res)

# # elif mode == "📖 Story RAG":
# #     st.subheader("📖 Long Story Assistant")
# #     story = st.text_area("Paste Story", height=250) #
# #     q = st.text_input("Question")
# #     if st.button("Analyze Story"):
# #         splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=100) #
# #         chunks = splitter.create_documents([story])
# #         # Retrieve best chunk
# #         best_chunk = max(chunks, key=lambda c: nlp(q).similarity(nlp(c.page_content)))
# #         res = llm.invoke(f"Context: {best_chunk.page_content}\nQuestion: {q}") #
# #         st.write(res)

# import streamlit as st
# import ollama
# import fitz  # PyMuPDF
# import os
# import json
# import tempfile
# import spacy
# import sys
# import io
# from datetime import datetime
# from langchain_ollama import OllamaLLM 
# from langchain_core.prompts import PromptTemplate
# from langchain_text_splitters import RecursiveCharacterTextSplitter
# import whisper
# from pydub import AudioSegment

# # ─── 1. SYSTEM & COMPATIBILITY CONFIG ─────────────────────────────────────────
# ffmpeg_folder = r'C:\ffmpeg\bin' 
# os.environ["PATH"] += os.pathsep + ffmpeg_folder
# AudioSegment.converter = os.path.join(ffmpeg_folder, "ffmpeg.exe")
# AudioSegment.ffprobe   = os.path.join(ffmpeg_folder, "ffprobe.exe")

# try:
#     import audioop
# except ImportError:
#     try:
#         import audioop_lts as audioop
#         sys.modules["audioop"] = audioop
#     except ImportError:
#         pass 

# # ─── 2. GLOBAL SETTINGS & STYLING ─────────────────────────────────────────────
# st.set_page_config(page_title="SignalZero", page_icon="⚡", layout="wide")

# st.markdown("""
# <style>
#     @import url('https://fonts.googleapis.com/css2?family=Space+Mono&family=Syne:wght@700&display=swap');
#     :root { --accent: #00c8ff; --bg: #080d1a; --surface: #0d1526; }
#     .stApp { background-color: var(--bg); color: #e8edf5; }
#     [data-testid="stSidebar"] { background-color: var(--surface); border-right: 1px solid #1a2540; }
#     .stButton>button { border: 1px solid var(--accent); color: var(--accent); background: transparent; font-family: 'Space Mono'; border-radius: 2px; }
#     .stButton>button:hover { background: var(--accent); color: var(--bg); }
#     .answer-box { background: var(--surface); border-left: 3px solid var(--accent); padding: 15px; border-radius: 0 5px 5px 0; font-family: 'Space Mono'; font-size: 13px; }
#     .stTextArea textarea { background-color: var(--surface) !important; color: white !important; border: 1px solid #1a2540 !important; }
# </style>
# """, unsafe_allow_html=True)

# # ─── 3. SHARED RESOURCE LOADING ───────────────────────────────────────────────
# @st.cache_resource
# def get_models():
#     try:
#         nlp = spacy.load("en_core_web_md")
#     except:
#         nlp = None
#     whisper_model = whisper.load_model("base")
#     llm = OllamaLLM(model='llama3.1:8b')
#     return nlp, whisper_model, llm

# nlp, whisper_model, llm = get_models()

# # ─── 4. SIDEBAR NAVIGATION ──────────────────────────────────────────────────
# with st.sidebar:
#     st.markdown("<h1 style='color: #00c8ff; font-family: Syne;'>⚡ SIGNALZERO</h1>", unsafe_allow_html=True)
#     mode = st.radio("SELECT MODULE", [
#         "🏠 Home", "📄 PDF Chat", "🎥 Video Chat", "🖼️ Image Describer", 
#         "🐍 Code Assist", "🗒️ Note Keeper", "📔 Diary Chat", "📖 Story RAG"
#     ])
#     st.divider()
#     st.caption("OFFLINE AI ENGINE v1.0")

# # ─── 5. MODULE LOGIC ─────────────────────────────────────────────────────────

# if mode == "🏠 Home":
#     st.title("Your AI. Anywhere.")
#     st.write("Welcome to the **SignalZero** workstation. No internet, no trackers, just raw local compute.")
#     st.info("Ensure Ollama is running in the background before using any chat modules.")

# elif mode == "📄 PDF Chat":
#     st.subheader("📄 Chat with PDF")
#     up_pdf = st.file_uploader("Upload PDF", type="pdf")
#     if up_pdf:
#         doc = fitz.open(stream=up_pdf.read(), filetype="pdf")
#         text = "".join([p.get_text() for p in doc])
#         q = st.text_input("What would you like to know about this document?")
#         if st.button("Query PDF") and q:
#             with st.spinner("Analyzing document..."):
#                 res = ollama.generate(model='llama3.1:8b', prompt=f"Context: {text[:10000]}\nQuestion: {q}")
#                 st.markdown(f"<div class='answer-box'>{res['response']}</div>", unsafe_allow_html=True)

# elif mode == "🎥 Video Chat":
#     st.subheader("🎥 Video AI Assistant")
#     up_vid = st.file_uploader("Upload MP4", type=["mp4"])
#     if up_vid:
#         with tempfile.NamedTemporaryFile(delete=False, suffix=".mp4") as t:
#             t.write(up_vid.read())
#             v_path = t.name
#         a_path = v_path.replace(".mp4", ".wav")
#         if 'v_transcript' not in st.session_state:
#             with st.spinner("Extracting audio and transcribing..."):
#                 AudioSegment.from_file(v_path).export(a_path, format="wav")
#                 st.session_state.v_transcript = whisper_model.transcribe(a_path)['text']
        
#         st.success("Video Processed")
#         with st.expander("View Transcript"):
#             st.write(st.session_state.v_transcript)
        
#         q = st.text_input("Ask a question about the video content")
#         if st.button("Ask Video AI") and q:
#             res = ollama.generate(model='llama3.1:8b', prompt=f"Transcript: {st.session_state.v_transcript}\nQuestion: {q}")
#             st.markdown(f"<div class='answer-box'>{res['response']}</div>", unsafe_allow_html=True)

# elif mode == "🖼️ Image Describer":
#     st.subheader("🖼️ Vision AI")
#     up_img = st.file_uploader("Upload Image", type=["jpg", "png", "jpeg"])
#     if up_img:
#         st.image(up_img, width=500)
#         if st.button("Describe Image"):
#             with st.spinner("LLava is looking..."):
#                 res = ollama.chat(model='llava:7b', messages=[{'role':'user','content':'Describe this image in detail.','images':[up_img.getvalue()]}])
#                 st.markdown(f"<div class='answer-box'>{res['message']['content']}</div>", unsafe_allow_html=True)

# elif mode == "🐍 Code Assist":
#     st.subheader("🐍 Self-Fixing Code Assist")
#     prompt_input = st.text_area("Write your coding prompt.", placeholder="e.g., Write a function to calculate Fibonacci numbers")
    
#     if "working_code" not in st.session_state:
#         st.session_state["working_code"] = ""

#     if st.button("Generate & Fix Code"):
#         if prompt_input:
#             current_prompt = prompt_input + "\nNote: Output must have only Python code. Do not add any explanation or text outside of the code block."
#             attempts, max_attempts = 0, 5
#             while attempts < max_attempts:
#                 attempts += 1
#                 st.write(f"⚙️ Attempt {attempts}...")
#                 response = ollama.generate(model='llama3.1:8b', prompt=current_prompt)
#                 code = response["response"].replace("```python", "").replace("```", "").strip()

#                 old_stdout = sys.stdout
#                 sys.stdout = buffer = io.StringIO()
#                 exec_error = None
#                 try:
#                     exec(code, {})
#                 except Exception as e:
#                     exec_error = str(e)
#                 sys.stdout = old_stdout
#                 output = buffer.getvalue()

#                 if exec_error:
#                     st.warning(f"Attempt {attempts} failed. Retrying...")
#                     current_prompt = f"The code produced an error: {exec_error}\nCode:\n{code}\nFix it and provide ONLY code."
#                 else:
#                     st.success("Code is working!")
#                     st.code(code, language='python')
#                     if output: st.text(f"Output:\n{output}")
#                     st.session_state["working_code"] = code
#                     break
    
#     st.divider()
#     st.subheader("Ask a Question about the Code")
#     c_q = st.text_input("What part should I explain?")
#     if st.button("Explain") and st.session_state["working_code"]:
#         with st.spinner("Thinking..."):
#             exp_prompt = f"Code:\n{st.session_state['working_code']}\n\nQuestion: {c_q}\nExplain in detail."
#             answer = ollama.generate(model='llama3.1:8b', prompt=exp_prompt)
#             st.info(answer["response"])

# elif mode == "🗒️ Note Keeper":
#     st.subheader("🗒️ Personal Knowledge Base")
#     with st.form("note_form", clear_on_submit=True):
#         note = st.text_area("New Note")
#         if st.form_submit_button("Save Note") and note:
#             with open("note.text", "a") as f: f.write(f"\n\n{note}")
#             st.toast("Note stored.")
    
#     q = st.text_input("Query your notes")
#     if st.button("Ask AI") and os.path.exists("note.text"):
#         with open("note.text", "r") as f: context = f.read()
#         res = llm.invoke(f"Context: {context}\nQuestion: {q}")
#         st.markdown(f"<div class='answer-box'>{res}</div>", unsafe_allow_html=True)

# elif mode == "📔 Diary Chat":
#     st.subheader("📔 Private Diary Chat")
#     d_date = st.date_input("Date", value=datetime.now())
#     with st.form("diary_entry", clear_on_submit=True):
#         entry = st.text_area("How was your day?")
#         if st.form_submit_button("Save Entry") and entry:
#             data = json.load(open("diary.json")) if os.path.exists("diary.json") else {}
#             data[str(d_date)] = entry
#             json.dump(data, open("diary.json", "w"), indent=4)
#             st.toast("Entry saved.")
    
#     q = st.text_input("Recall a memory")
#     if st.button("Search Diary") and os.path.exists("diary.json"):
#         data = json.load(open("diary.json"))
#         context = "\n".join([f"{k}: {v}" for k,v in data.items()])
#         res = llm.invoke(f"Diary Entries: {context}\nQuestion: {q}")
#         st.markdown(f"<div class='answer-box'>{res}</div>", unsafe_allow_html=True)

# elif mode == "📖 Story RAG":
#     st.subheader("📖 Smart Story Assistant")
#     story = st.text_area("Paste long story here", height=250)
#     q = st.text_input("Ask a question about the plot")
#     if st.button("Analyze Story") and story and q:
#         with st.spinner("Processing story..."):
#             splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=150)
#             chunks = splitter.create_documents([story])
#             # Basic Similarity search
#             best_chunk = chunks[0].page_content
#             if nlp:
#                 q_vec = nlp(q)
#                 best_chunk = max(chunks, key=lambda c: q_vec.similarity(nlp(c.page_content))).page_content
            
#             res = llm.invoke(f"Context: {best_chunk}\nQuestion: {q}")
#             st.markdown(f"<div class='answer-box'>{res}</div>", unsafe_allow_html=True)


import streamlit as st
import ollama
import fitz  # PyMuPDF
import os
import json
import tempfile
import spacy
import sys
import io
from datetime import datetime
from langchain_ollama import OllamaLLM
from langchain_core.prompts import PromptTemplate
from langchain_text_splitters import RecursiveCharacterTextSplitter
import whisper
from pydub import AudioSegment

# ─── 1. SYSTEM & COMPATIBILITY CONFIG ─────────────────────────────────────────
ffmpeg_folder = r'C:\ffmpeg\bin'
os.environ["PATH"] += os.pathsep + ffmpeg_folder
AudioSegment.converter = os.path.join(ffmpeg_folder, "ffmpeg.exe")
AudioSegment.ffprobe   = os.path.join(ffmpeg_folder, "ffprobe.exe")

try:
    import audioop
except ImportError:
    try:
        import audioop_lts as audioop
        sys.modules["audioop"] = audioop
    except ImportError:
        pass

# ─── 2. PAGE CONFIG ───────────────────────────────────────────────────────────
st.set_page_config(
    page_title="SignalZero — Offline AI",
    page_icon="⚡",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ─── 3. GLOBAL CSS ────────────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Space+Mono:wght@400;700&family=Syne:wght@400;700;800&display=swap');

:root {
    --bg: #060b17;
    --surface: #0b1120;
    --surface2: #0f1729;
    --border: #161f35;
    --accent: #00c8ff;
    --accent-dim: rgba(0,200,255,0.12);
    --accent-glow: rgba(0,200,255,0.25);
    --text: #dde4f0;
    --muted: #3d4f6e;
    --success: #00e87a;
    --warning: #ffaa00;
}

/* Base */
html, body, [class*="css"], .stApp {
    background-color: var(--bg) !important;
    color: var(--text) !important;
    font-family: 'Syne', sans-serif;
}

/* Sidebar */
[data-testid="stSidebar"] {
    background: var(--surface) !important;
    border-right: 1px solid var(--border) !important;
}
[data-testid="stSidebar"] * { color: var(--text) !important; }

/* Hide clutter */
#MainMenu, footer, header { visibility: hidden; }
.block-container { padding-top: 0.5rem !important; }

/* Buttons */
.stButton > button {
    background: transparent !important;
    border: 1px solid var(--accent) !important;
    color: var(--accent) !important;
    font-family: 'Space Mono', monospace !important;
    font-size: 11px !important;
    letter-spacing: 2px !important;
    padding: 10px 24px !important;
    border-radius: 2px !important;
    transition: all 0.15s ease !important;
    text-transform: uppercase !important;
}
.stButton > button:hover {
    background: var(--accent) !important;
    color: var(--bg) !important;
    box-shadow: 0 0 20px var(--accent-glow) !important;
}

/* Inputs */
.stTextInput > div > div > input,
.stTextArea > div > div > textarea {
    background: var(--surface2) !important;
    border: 1px solid var(--border) !important;
    color: var(--text) !important;
    font-family: 'Space Mono', monospace !important;
    font-size: 13px !important;
    border-radius: 2px !important;
    transition: border-color 0.15s !important;
}
.stTextInput > div > div > input:focus,
.stTextArea > div > div > textarea:focus {
    border-color: var(--accent) !important;
    box-shadow: 0 0 0 1px var(--accent) !important;
}

/* Labels */
label, .stTextInput label, .stTextArea label {
    color: var(--muted) !important;
    font-family: 'Space Mono', monospace !important;
    font-size: 10px !important;
    letter-spacing: 2px !important;
    text-transform: uppercase !important;
}

/* Radio */
.stRadio > div { gap: 4px !important; }
.stRadio label {
    text-transform: none !important;
    letter-spacing: 0 !important;
    font-size: 13px !important;
    font-family: 'Syne', sans-serif !important;
    padding: 6px 10px !important;
    border-radius: 2px !important;
    transition: background 0.1s !important;
}
.stRadio label:hover { background: var(--accent-dim) !important; }

/* Form submit */
.stFormSubmitButton > button {
    background: transparent !important;
    border: 1px solid var(--success) !important;
    color: var(--success) !important;
    font-family: 'Space Mono', monospace !important;
    font-size: 11px !important;
    letter-spacing: 2px !important;
    text-transform: uppercase !important;
}
.stFormSubmitButton > button:hover {
    background: var(--success) !important;
    color: var(--bg) !important;
}

/* File uploader */
[data-testid="stFileUploader"] {
    background: var(--surface2) !important;
    border: 1px dashed var(--border) !important;
    border-radius: 2px !important;
}

/* Divider */
hr { border-color: var(--border) !important; margin: 28px 0 !important; }

/* Expander */
.streamlit-expanderHeader {
    background: var(--surface2) !important;
    border: 1px solid var(--border) !important;
    font-family: 'Space Mono', monospace !important;
    font-size: 12px !important;
}

/* Scrollbar */
::-webkit-scrollbar { width: 3px; }
::-webkit-scrollbar-track { background: var(--bg); }
::-webkit-scrollbar-thumb { background: var(--border); border-radius: 2px; }
::-webkit-scrollbar-thumb:hover { background: var(--accent); }

/* Custom components */
.answer-box {
    background: var(--surface2);
    border-left: 3px solid var(--accent);
    padding: 18px 22px;
    margin-top: 16px;
    border-radius: 0 3px 3px 0;
    font-family: 'Space Mono', monospace;
    font-size: 13px;
    line-height: 1.85;
    color: var(--text);
}

.pill {
    display: inline-block;
    background: var(--accent-dim);
    border: 1px solid rgba(0,200,255,0.25);
    color: var(--accent);
    font-family: 'Space Mono', monospace;
    font-size: 9px;
    letter-spacing: 2px;
    padding: 3px 10px;
    border-radius: 20px;
    margin: 2px;
    text-transform: uppercase;
}

.tool-card {
    background: var(--surface);
    border: 1px solid var(--border);
    border-top: 2px solid var(--accent);
    padding: 22px;
    border-radius: 3px;
    margin-bottom: 16px;
    transition: border-color 0.2s, box-shadow 0.2s;
    height: 100%;
}
.tool-card:hover {
    border-color: var(--accent);
    box-shadow: 0 0 20px rgba(0,200,255,0.08);
}

.stat-box {
    background: var(--surface);
    border: 1px solid var(--border);
    padding: 16px 20px;
    border-radius: 3px;
    text-align: center;
}

.section-label {
    font-family: 'Space Mono', monospace;
    font-size: 10px;
    color: var(--accent);
    letter-spacing: 3px;
    text-transform: uppercase;
    margin-bottom: 8px;
}

.page-title {
    font-family: 'Syne', sans-serif;
    font-weight: 800;
    font-size: 30px;
    color: var(--text);
    letter-spacing: -1px;
    margin-bottom: 6px;
}

.page-sub {
    font-family: 'Space Mono', monospace;
    font-size: 12px;
    color: var(--muted);
    margin-bottom: 24px;
}
</style>
""", unsafe_allow_html=True)

# ─── 4. LOAD MODELS ───────────────────────────────────────────────────────────
@st.cache_resource
def get_models():
    try:
        nlp = spacy.load("en_core_web_md")
    except Exception:
        nlp = None
    whisper_model = whisper.load_model("base")
    llm = OllamaLLM(model='llama3.1:8b')
    return nlp, whisper_model, llm

nlp, whisper_model, llm = get_models()

# ─── 5. SIDEBAR ───────────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown("""
    <div style='padding: 24px 8px 16px 8px;'>
        <div style='font-family: Space Mono, monospace; font-size: 10px;
                    color: #00c8ff; letter-spacing: 4px; margin-bottom: 2px;'>
            ⚡ SIGNAL
        </div>
        <div style='font-family: Syne, sans-serif; font-size: 36px;
                    font-weight: 800; color: #dde4f0; letter-spacing: -2px; line-height:1;'>
            Zero
        </div>
        <div style='font-family: Space Mono, monospace; font-size: 9px;
                    color: #3d4f6e; letter-spacing: 1.5px; margin-top: 6px;'>
            OFFLINE AI TOOLKIT v1.0
        </div>
    </div>
    <hr style='border-color: #161f35; margin: 8px 0 16px 0;'/>
    <div style='font-family: Space Mono, monospace; font-size: 9px;
                color: #3d4f6e; letter-spacing: 2px; margin-bottom: 10px; padding-left: 4px;'>
        MODULES
    </div>
    """, unsafe_allow_html=True)

    mode = st.radio(
        label="",
        options=[
            "🏠  Home",
            "📄  PDF Chat",
            "🎥  Video Chat",
            "🖼️  Image Describer",
            "🐍  Code Assist",
            "🗒️  Note Keeper",
            "📔  Diary Chat",
            "📖  Story RAG",
        ],
        label_visibility="collapsed"
    )

    st.markdown("""
    <hr style='border-color: #161f35; margin: 20px 0 14px 0;'/>
    <div style='font-family: Space Mono, monospace; font-size: 9px;
                color: #1e2a40; line-height: 2; padding-left: 4px;'>
        NO INTERNET REQUIRED<br/>
        NO API KEYS<br/>
        NO DATA LEAVES YOUR MACHINE<br/>
        FREE FOREVER
    </div>
    <div style='margin-top: 16px; padding-left: 4px;'>
        <div style='font-family: Space Mono, monospace; font-size: 9px; color: #3d4f6e;'>
            BUILT BY
        </div>
        <div style='font-family: Syne, sans-serif; font-size: 13px;
                    font-weight: 700; color: #00c8ff; margin-top: 2px;'>
            Anmol Srivastava
        </div>
        <div style='font-family: Space Mono, monospace; font-size: 9px;
                    color: #3d4f6e; margin-top: 2px;'>
            TCS · NATWEST BANK UK
        </div>
    </div>
    """, unsafe_allow_html=True)

# ─── HELPER ───────────────────────────────────────────────────────────────────
def page_header(title, subtitle=""):
    st.markdown(f"""
    <div style='margin-bottom: 20px; padding-top: 8px;'>
        <div class='section-label'>⚡ SIGNALZERO</div>
        <div class='page-title'>{title}</div>
        {"<div class='page-sub'>" + subtitle + "</div>" if subtitle else ""}
    </div>
    """, unsafe_allow_html=True)

# ══════════════════════════════════════════════════════════════════════════════
# 🏠 HOME
# ══════════════════════════════════════════════════════════════════════════════
if mode == "🏠  Home":

    # Hero — compact, fits in one screenshot
    st.markdown("""
    <div style='padding: 28px 0 24px 0;'>
        <div style='font-family: Space Mono, monospace; font-size: 10px;
                    color: #00c8ff; letter-spacing: 4px; margin-bottom: 10px;'>
            ⚡ SIGNALZERO — OFFLINE AI TOOLKIT v1.0
        </div>
        <div style='font-family: Syne, sans-serif; font-size: 44px; font-weight: 800;
                    color: #dde4f0; line-height: 1.05; letter-spacing: -2px; margin-bottom: 12px;'>
            Your AI. <span style='color: #00c8ff;'>Anywhere.</span>
        </div>
        <div style='font-family: Space Mono, monospace; font-size: 11px;
                    color: #3d4f6e; line-height: 1.9; margin-bottom: 16px;'>
            Built after getting stuck on a plane with no internet. Most AI breaks when the signal drops.<br/>
            SignalZero runs 7 tools fully offline — no internet, no API keys, no data leaving your machine.
        </div>
        <div style='margin-bottom: 4px;'>
            <span class='pill'>NO INTERNET</span>
            <span class='pill'>NO API KEYS</span>
            <span class='pill'>NO CLOUD</span>
            <span class='pill'>ZERO COST</span>
            <span class='pill'>PRIVATE</span>
        </div>
    </div>
    <hr style='margin: 16px 0 20px 0 !important;'/>
    """, unsafe_allow_html=True)

    # Tool grid — compact cards, icon + name only
    tools = [
        ("📄", "PDF Chat"),
        ("🎥", "Video Chat"),
        ("🖼️", "Image Describer"),
        ("🐍", "Code Assist"),
        ("🗒️", "Note Keeper"),
        ("📔", "Diary Chat"),
        ("📖", "Story RAG"),
    ]

    st.markdown("<div class='section-label' style='margin-bottom:14px;'>AVAILABLE MODULES</div>",
                unsafe_allow_html=True)

    cols = st.columns(4)
    for i, (icon, title) in enumerate(tools):
        with cols[i % 4]:
            st.markdown(f"""
            <div style='background: #0b1120; border: 1px solid #161f35;
                        border-top: 2px solid #00c8ff; padding: 16px 14px;
                        border-radius: 3px; margin-bottom: 12px; text-align: center;'>
                <div style='font-size: 22px; margin-bottom: 8px;'>{icon}</div>
                <div style='font-family: Syne, sans-serif; font-weight: 700;
                            font-size: 13px; color: #dde4f0;'>{title}</div>
            </div>
            """, unsafe_allow_html=True)

    # Stack — one line
    st.markdown("""
    <hr style='margin: 8px 0 12px 0 !important;'/>
    <div style='display: flex; gap: 32px; align-items: center; flex-wrap: wrap;'>
        <div>
            <div class='section-label' style='margin-bottom: 10px;'>POWERED BY</div>
            <div>
                <span class='pill'>LLaMA 3.1:8b</span>
                <span class='pill'>LLaVA 7b</span>
                <span class='pill'>Whisper</span>
                <span class='pill'>LangChain</span>
                <span class='pill'>SpaCy</span>
                <span class='pill'>Ollama</span>
                <span class='pill'>Streamlit</span>
            </div>
        </div>
    </div>
    <div style='margin-top: 20px; font-family: Space Mono, monospace;
                font-size: 10px; color: #1e2a40;'>
        SIGNALZERO v1.0 · BUILT IN PUBLIC · OPEN SOURCE
    </div>
    """, unsafe_allow_html=True)

# ══════════════════════════════════════════════════════════════════════════════
# 📄 PDF CHAT
# ══════════════════════════════════════════════════════════════════════════════
elif mode == "📄  PDF Chat":
    page_header("PDF Chat", "Upload a PDF — ask anything about it locally")

    up_pdf = st.file_uploader("Upload PDF", type="pdf")
    if up_pdf:
        doc = fitz.open(stream=up_pdf.read(), filetype="pdf")
        text = "".join([p.get_text() for p in doc])
        st.markdown(f"""
        <div class='pill'>✓ LOADED</div>
        <div class='pill'>{len(doc)} PAGES</div>
        <div class='pill'>{len(text):,} CHARS</div>
        """, unsafe_allow_html=True)
        st.markdown("<br/>", unsafe_allow_html=True)
        q = st.text_input("What would you like to know about this document?")
        if st.button("Query PDF") and q:
            with st.spinner("Analyzing..."):
                res = ollama.generate(
                    model='llama3.1:8b',
                    prompt=f"Context: {text[:10000]}\nQuestion: {q}\nAnswer based only on the context."
                )
                st.markdown(f"<div class='answer-box'>{res['response']}</div>", unsafe_allow_html=True)
    else:
        st.info("Upload a PDF to get started.")

# ══════════════════════════════════════════════════════════════════════════════
# 🎥 VIDEO CHAT
# ══════════════════════════════════════════════════════════════════════════════
elif mode == "🎥  Video Chat":
    page_header("Video Chat", "Transcribe via Whisper locally — then chat with the content")

    up_vid = st.file_uploader("Upload MP4", type=["mp4"])
    if up_vid:
        with tempfile.NamedTemporaryFile(delete=False, suffix=".mp4") as t:
            t.write(up_vid.read())
            v_path = t.name
        a_path = v_path.replace(".mp4", ".wav")

        if 'v_transcript' not in st.session_state:
            with st.spinner("Extracting audio and transcribing..."):
                AudioSegment.from_file(v_path).export(a_path, format="wav")
                st.session_state.v_transcript = whisper_model.transcribe(a_path)['text']

        st.markdown("<div class='pill'>✓ TRANSCRIBED</div><br/>", unsafe_allow_html=True)
        with st.expander("View Full Transcript"):
            st.markdown(f"<div class='answer-box'>{st.session_state.v_transcript}</div>",
                        unsafe_allow_html=True)

        q = st.text_input("Ask a question about the video content")
        if st.button("Ask Video AI") and q:
            with st.spinner("Thinking..."):
                res = ollama.generate(
                    model='llama3.1:8b',
                    prompt=f"Transcript: {st.session_state.v_transcript}\nQuestion: {q}"
                )
                st.markdown(f"<div class='answer-box'>{res['response']}</div>", unsafe_allow_html=True)

# ══════════════════════════════════════════════════════════════════════════════
# 🖼️ IMAGE DESCRIBER
# ══════════════════════════════════════════════════════════════════════════════
elif mode == "🖼️  Image Describer":
    page_header("Image Describer", "Upload images — get AI descriptions via LLaVA 7b")

    up_img = st.file_uploader("Upload Image", type=["jpg", "png", "jpeg"],
                               accept_multiple_files=True)
    if up_img:
        for img in up_img:
            col1, col2 = st.columns([1, 1])
            with col1:
                st.image(img, caption=img.name, use_container_width=True)
            with col2:
                with st.spinner("LLaVA is analyzing..."):
                    try:
                        res = ollama.chat(
                            model='llava:7b',
                            messages=[{
                                'role': 'user',
                                'content': 'Describe this image in detail.',
                                'images': [img.getvalue()]
                            }]
                        )
                        st.markdown(f"""
                        <div class='section-label' style='margin-top:8px;'>AI DESCRIPTION</div>
                        <div class='answer-box'>{res['message']['content']}</div>
                        """, unsafe_allow_html=True)
                    except Exception as e:
                        st.error(f"Error: {e}")
                        st.info("Run: ollama pull llava")
            st.markdown("<hr/>", unsafe_allow_html=True)
    else:
        st.info("Upload one or more images to get started.")

# ══════════════════════════════════════════════════════════════════════════════
# 🐍 CODE ASSIST
# ══════════════════════════════════════════════════════════════════════════════
elif mode == "🐍  Code Assist":
    page_header("Python Code Assist", "Generate, auto-fix (5x), and explain Python code locally")

    if "working_code" not in st.session_state:
        st.session_state["working_code"] = ""

    prompt_input = st.text_area(
        "Write your coding prompt",
        placeholder="e.g., Write a function to calculate Fibonacci numbers",
        height=120
    )

    if st.button("Generate & Fix Code"):
        if prompt_input:
            current_prompt = prompt_input + "\nNote: Output must have only Python code. No explanation outside the code block."
            attempts, max_attempts = 0, 5
            while attempts < max_attempts:
                attempts += 1
                st.write(f"⚙️ Attempt {attempts}...")
                response = ollama.generate(model='llama3.1:8b', prompt=current_prompt)
                code = response["response"].replace("```python", "").replace("```", "").strip()

                old_stdout = sys.stdout
                sys.stdout = buffer = io.StringIO()
                exec_error = None
                try:
                    exec(code, {})
                except Exception as e:
                    exec_error = str(e)
                sys.stdout = old_stdout
                output = buffer.getvalue()

                if exec_error:
                    st.warning(f"Attempt {attempts} failed — auto-fixing...")
                    current_prompt = f"Error: {exec_error}\nCode:\n{code}\nFix it. Return ONLY corrected Python code."
                    if attempts == max_attempts:
                        st.error("Could not fix after 5 attempts. Try rephrasing your prompt.")
                else:
                    st.success("✓ Code is working!")
                    st.code(code, language='python')
                    if output:
                        st.markdown(f"<div class='answer-box'><b>Output:</b><br/>{output}</div>",
                                    unsafe_allow_html=True)
                    st.session_state["working_code"] = code
                    break

    st.markdown("<hr/>", unsafe_allow_html=True)
    st.markdown("<div class='section-label'>Ask About The Code</div>", unsafe_allow_html=True)

    c_q = st.text_input("What part should I explain?")
    if st.button("Explain Code"):
        if st.session_state["working_code"]:
            with st.spinner("Thinking..."):
                exp_prompt = f"Code:\n{st.session_state['working_code']}\n\nQuestion: {c_q}\nExplain in detail."
                answer = ollama.generate(model='llama3.1:8b', prompt=exp_prompt)
                st.markdown(f"<div class='answer-box'>{answer['response']}</div>",
                            unsafe_allow_html=True)
        else:
            st.warning("Generate working code first!")

# ══════════════════════════════════════════════════════════════════════════════
# 🗒️ NOTE KEEPER
# ══════════════════════════════════════════════════════════════════════════════
elif mode == "🗒️  Note Keeper":
    page_header("Note Keeper", "Build your personal knowledge base — query it anytime")

    if not os.path.exists("note.text"):
        open("note.text", "w").close()

    with st.form("note_form", clear_on_submit=True):
        note = st.text_area("Add a new note", height=150)
        submitted = st.form_submit_button("Save Note")

    if submitted and note:
        with open("note.text", "a") as f:
            f.write(f"\n\n{note}")
        st.success("Note saved.")

    with open("note.text", "r") as f:
        content = f.read()
    count = len([n for n in content.split("\n\n") if n.strip()])
    st.markdown(f"<div class='pill'>{count} NOTES STORED</div><br/>", unsafe_allow_html=True)

    st.markdown("<hr/>", unsafe_allow_html=True)
    q = st.text_input("Query your notes")
    if st.button("Ask AI") and q:
        with st.spinner("Searching..."):
            res = llm.invoke(f"Context:\n{content}\n\nQuestion: {q}\nAnswer based only on the notes.")
            st.markdown(f"<div class='answer-box'>{res}</div>", unsafe_allow_html=True)

# ══════════════════════════════════════════════════════════════════════════════
# 📔 DIARY CHAT
# ══════════════════════════════════════════════════════════════════════════════
elif mode == "📔  Diary Chat":
    page_header("Diary Chat", "Private diary — searchable, queryable, never leaves your machine")

    if not os.path.exists("diary.json"):
        json.dump({}, open("diary.json", "w"))

    d_date = st.date_input("Entry date", value=datetime.now())

    with st.form("diary_entry", clear_on_submit=True):
        entry = st.text_area("Write your entry", height=180)
        submitted = st.form_submit_button("Save Entry")

    if submitted and entry:
        data = json.load(open("diary.json"))
        data[str(d_date)] = entry
        json.dump(data, open("diary.json", "w"), indent=4)
        st.success(f"Entry saved for {d_date}")

    data = json.load(open("diary.json"))
    st.markdown(f"<div class='pill'>{len(data)} ENTRIES</div><br/>", unsafe_allow_html=True)

    st.markdown("<hr/>", unsafe_allow_html=True)
    q = st.text_input("Search your diary")
    if st.button("Search Diary") and q:
        with st.spinner("Searching memories..."):
            context = "\n\n".join([f"[{k}]: {v}" for k, v in data.items()])
            res = llm.invoke(f"Diary:\n{context}\n\nQuestion: {q}")
            st.markdown(f"<div class='answer-box'>{res}</div>", unsafe_allow_html=True)

# ══════════════════════════════════════════════════════════════════════════════
# 📖 STORY RAG
# ══════════════════════════════════════════════════════════════════════════════
elif mode == "📖  Story RAG":
    page_header("Story RAG", "Paste any long text — ask smart questions using chunked RAG")

    story = st.text_area("Paste long text here", height=250)

    if story:
        word_count = len(story.split())
        st.markdown(f"<div class='pill'>{word_count:,} WORDS</div><br/>", unsafe_allow_html=True)

        q = st.text_input("Ask a question about the text")
        if st.button("Analyze") and q:
            with st.spinner("Processing..."):
                splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=150)
                chunks = splitter.create_documents([story])
                best_chunk = chunks[0].page_content
                if nlp:
                    q_vec = nlp(q)
                    best_chunk = max(
                        chunks, key=lambda c: q_vec.similarity(nlp(c.page_content))
                    ).page_content
                res = llm.invoke(f"Context: {best_chunk}\nQuestion: {q}")
                st.markdown(f"<div class='answer-box'>{res}</div>", unsafe_allow_html=True)