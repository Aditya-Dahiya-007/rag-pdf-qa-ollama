import streamlit as st
import time
import requests
from typing import List, Dict, Any
from datetime import datetime

# CONFIG
BACKEND_URL = "http://localhost:5050"

# Page config
st.set_page_config(
    page_title="📚 PDF Intelligence Hub",
    page_icon="📚",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Inject CSS for styling
st.markdown("""
<style>
    .main-header {
        background: linear-gradient(90deg, #667eea 0%, #764ba2 100%);
        padding: 1rem;
        border-radius: 10px;
        margin-bottom: 2rem;
        color: white;
        text-align: center;
    }
</style>
""", unsafe_allow_html=True)

# Initialize session state
if 'chat_history' not in st.session_state:
    st.session_state.chat_history = []
if 'uploaded_files' not in st.session_state:
    st.session_state.uploaded_files = []
if 'uploaded_file_names' not in st.session_state:
    st.session_state.uploaded_file_names = set()
if 'processed_file_names' not in st.session_state:
    st.session_state.processed_file_names = set()

# HEADER
st.markdown("""
<div class="main-header">
    <h1>📚 PDF Intelligence Hub</h1>
    <p>Advanced semantic search and Q&A for your documents</p>
</div>
""", unsafe_allow_html=True)

# SIDEBAR: Configuration
with st.sidebar:
    st.markdown("## 🔧 Settings")
    if st.button("🧹 Clear Chat"):
        st.session_state.chat_history = []
        st.rerun()
    if st.button("🗑️ Remove All PDFs"):
        st.session_state.uploaded_files = []
        st.session_state.uploaded_file_names = set()
        st.session_state.processed_file_names = set()
        st.success("Cleared uploaded documents.")
        st.rerun()

# MAIN AREA
st.markdown("### 📄 Upload PDFs")
uploaded_files = st.file_uploader("Upload one or more PDFs", type="pdf", accept_multiple_files=True)

if uploaded_files:
    for file in uploaded_files:
        if file.name not in st.session_state.uploaded_file_names:
            st.session_state.uploaded_files.append(file)
            st.session_state.uploaded_file_names.add(file.name)

# Identify unprocessed files
unprocessed_files = [file for file in st.session_state.uploaded_files if file.name not in st.session_state.processed_file_names]

if unprocessed_files:
    if st.button("🔄 Process All Unprocessed PDFs"):
        with st.spinner("Processing PDFs..."):
            for file in unprocessed_files:
                files = {"file": (file.name, file, "application/pdf")}
                res = requests.post(f"{BACKEND_URL}/upload", files=files)
                if res.ok:
                    st.success(f"Uploaded {file.name}")
                    st.session_state.processed_file_names.add(file.name)
                else:
                    st.error(f"Failed to upload {file.name}")

# CHAT AREA
st.markdown("### 🔍 Ask a Question")
question = st.text_input("Type your question below")

if st.button("🚀 Ask") and question:
    if not st.session_state.processed_file_names:
        st.warning("Please process PDFs before asking questions.")
    else:
        st.session_state.chat_history.append({"role": "user", "content": question})
        with st.spinner("Thinking..."):
            response = requests.post(f"{BACKEND_URL}/ask", json={"question": question})
            if response.ok:
                answer = response.json().get("answer", "No answer returned.")
                st.session_state.chat_history.append({"role": "assistant", "content": answer})
            else:
                st.error("Failed to get response from the backend.")

# DISPLAY CHAT HISTORY
for msg in st.session_state.chat_history:
    if msg['role'] == 'user':
        st.markdown(f"**You:** {msg['content']}")
    else:
        st.markdown(f"**Assistant:** {msg['content']}")
