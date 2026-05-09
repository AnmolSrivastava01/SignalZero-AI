# ⚡ SignalZero
### AI that works at zero signal.

> Built after getting stuck on a plane with no internet — and realizing that most "AI-powered workflows" completely break without connectivity.

SignalZero is a fully offline AI toolkit that runs 6 powerful tools entirely on your local machine. No internet. No API keys. No cloud dependency. No cost.

---

## 🛠️ Tools

| Tool | Description |
|------|-------------|
| 📄 **Chat with PDF** | Upload any PDF and ask questions about it |
| 🎥 **Chat with Video** | Transcribes video audio via Whisper, then lets you chat with the content |
| 🖼️ **Image Describer** | Upload images and get detailed AI descriptions |
| 📝 **Chat with Notes** | Build a personal knowledge base and query it anytime |
| 📔 **Chat with Diary** | Date-based diary with semantic search across all entries |
| 📖 **Story Q&A** | Paste any long text and ask smart questions using RAG |

---

## 🚀 Getting Started

### 1. Install Ollama
Download from [ollama.ai](https://ollama.ai) and pull the required models:
```bash
ollama pull llama3.1
ollama pull llava:7b
```

### 2. Install Dependencies
```bash
pip install streamlit langchain langchain-community ollama PyMuPDF spacy openai-whisper pydub opencv-python numpy
python -m spacy download en_core_web_md
```

> **Note:** You also need `ffmpeg` installed for video/audio processing.
> - Windows: Download from [ffmpeg.org](https://ffmpeg.org)
> - Mac: `brew install ffmpeg`
> - Linux: `sudo apt install ffmpeg`

### 3. Run
```bash
streamlit run app.py
```

---

## 🧠 How It Works

SignalZero uses **Retrieval-Augmented Generation (RAG)** to answer questions accurately:

1. **Split** — Large documents are chunked into manageable pieces
2. **Search** — SpaCy embeddings find the most relevant chunks for your question
3. **Answer** — Only relevant chunks are sent to the local LLM — saving compute and improving accuracy

All processing happens **on your device**. No data leaves your machine.

---

## 📦 Tech Stack

- **LLM** — LLaMA 3.1 via Ollama (fully local)
- **Vision** — LLaVA 7B for image understanding
- **Speech** — OpenAI Whisper (runs locally)
- **RAG** — LangChain + SpaCy embeddings
- **UI** — Streamlit

---

## 💡 Why SignalZero?

Most AI tools assume you have internet. SignalZero was built for:
- ✈️ Flights and travel
- 🏔️ Remote locations
- 🔒 Privacy-sensitive environments
- 💰 Zero API cost workflows

---

## 👨‍💻 Built By

**Anmol Srivastava** — Agentic AI Developer at TCS, building production multi-agent systems for NatWest Bank (UK).

[LinkedIn](https://linkedin.com/in/anmolsrivastava) · [GitHub](https://github.com/anmolsrivastava)

---

⭐ Star this repo if you found it useful. Built in public — follow along for updates.
