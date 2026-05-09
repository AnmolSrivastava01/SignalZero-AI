import os
import sys
import shutil
import tempfile
import streamlit as st

# --- 1. FFMPEG ABSOLUTE CONFIGURATION ---
# We point directly to your renamed folder to avoid [WinError 2]
ffmpeg_folder = r'C:\ffmpeg\bin'

# Force the system to recognize the ffmpeg folder for this session
os.environ["PATH"] += os.pathsep + ffmpeg_folder

# Manually tell pydub exactly where the executables are
from pydub import AudioSegment
AudioSegment.converter = os.path.join(ffmpeg_folder, "ffmpeg.exe")
AudioSegment.ffprobe   = os.path.join(ffmpeg_folder, "ffprobe.exe")

# --- 2. PYTHON 3.13 AUDIOOP COMPATIBILITY ---
# Essential for Python 3.13 since built-in audioop was removed
try:
    import audioop
except ImportError:
    try:
        import audioop_lts as audioop
        sys.modules["audioop"] = audioop
    except ImportError:
        st.error("Missing 'audioop-lts'. Please run: pip install audioop-lts")

# Now safe to import remaining libraries
import whisper
import ollama

# --- 3. UI SETUP ---
st.set_page_config(page_title="Video AI Assistant", layout="wide")
st.title("🎙️ Chat with your Video Content")

# Quick link verification
if not os.path.exists(os.path.join(ffmpeg_folder, "ffmpeg.exe")):
    st.error(f"❌ FFMPEG not found at {ffmpeg_folder}. Please check your folder path!")
else:
    st.sidebar.success("✅ FFMPEG Linked")

# Load Whisper (Cached to save memory and time)
@st.cache_resource
def load_whisper_model():
    return whisper.load_model("base")

model = load_whisper_model()

# --- 4. CORE FUNCTIONS ---
def process_video_to_audio(uploaded_file):
    """Saves the uploaded video and extracts the audio track."""
    with tempfile.NamedTemporaryFile(delete=False, suffix=".mp4") as tmp_video:
        tmp_video.write(uploaded_file.read())
        video_path = tmp_video.name
    
    audio_path = video_path.replace(".mp4", ".wav")
    
    try:
        with st.spinner("Converting video to audio..."):
            audio = AudioSegment.from_file(video_path)
            audio.export(audio_path, format="wav")
        return audio_path
    except Exception as e:
        st.error(f"Audio Extraction Failed: {e}")
        return None

# --- 5. APP LOGIC ---
uploaded_video = st.file_uploader("Upload an MP4 video", type=["mp4"])

if uploaded_video:
    # Extract audio track
    audio_file = process_video_to_audio(uploaded_video)
    
    if audio_file:
        # Step 2: Transcribe using Whisper
        if 'transcript' not in st.session_state:
            with st.spinner("Transcribing audio (this may take a minute)..."):
                result = model.transcribe(audio_file)
                st.session_state.transcript = result['text']
        
        st.success("Transcription Complete!")
        with st.expander("Show Full Transcript"):
            st.write(st.session_state.transcript)

        # Step 3: Chat Interface
        st.divider()
        query = st.text_input("Ask a question about the video content:")
        
        if st.button("Ask AI"):
            if query:
                with st.spinner("Llama 3.1 is analyzing..."):
                    context = st.session_state.transcript
                    prompt = f"Using the following video transcript, answer the question.\n\nTranscript: {context}\n\nQuestion: {query}"
                    
                    # Generate response from Ollama
                    response = ollama.generate(model='llama3.1:8b', prompt=prompt)
                    
                    st.subheader("AI Answer:")
                    st.markdown(response['response'])
            else:
                st.warning("Please enter a question first.")

# Sidebar cleanup guide
st.sidebar.markdown("---")
st.sidebar.info("Requirements:\n- FFMPEG in C:\\ffmpeg\\bin\n- Ollama running locally\n- pip install audioop-lts")