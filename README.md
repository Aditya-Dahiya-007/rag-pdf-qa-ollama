# 📚 PDF Intelligence Hub (RAG with Ollama, Flask & Streamlit)

This project is a macOS-friendly **PDF Question Answering System** using:
- 🔍 **Semantic Search** with FAISS
- 🧠 **Local LLMs** via [Ollama](https://ollama.com/)
- ⚙️ Flask backend for document processing
- 💬 Streamlit frontend for chatting with documents

## 🚀 Features

- Upload and process **multiple PDFs**
- Ask questions in natural language
- RAG (Retrieval-Augmented Generation) system finds the best text chunks
- Works **offline** on macOS using local models like `llama3` with Ollama
- Designed to run entirely on-device (no API key required)

## 🧰 Tech Stack

- Python 3.10+
- [Streamlit](https://streamlit.io/)
- [Flask](https://flask.palletsprojects.com/)
- [PyMuPDF](https://pymupdf.readthedocs.io/) for PDF parsing
- [SentenceTransformers](https://www.sbert.net/) for embeddings
- [FAISS](https://github.com/facebookresearch/faiss) for vector search
- [Ollama](https://ollama.com/) for local LLMs

## 🖥️ Platform Support

| OS      | Status       | Notes                                 |
|---------|--------------|----------------------------------------|
| macOS   | ✅ Supported  | Natively works with Ollama + Python    |
| Linux   | ✅ Supported  | Install Ollama manually                |
| Windows | ⚠️ Partial   | Use WSL2 or adapt backend (no Ollama)  |

## 📦 Installation

1. Clone this repo:

```bash
git clone https://github.com/your-username/rag-pdf-qa-ollama.git
cd rag-pdf-qa-ollama
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
