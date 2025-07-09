from flask import Flask, request, jsonify
import os
import numpy as np
from utils.pdf_utils import extract_text_from_pdf, chunk_text
from embeddings.embedder import embed_chunks, build_vector_store
from retriever.vector_store import search
from llm.answer_generator import generate_answer
from sentence_transformers import SentenceTransformer

app = Flask(__name__)

from collections import defaultdict

all_chunks = []
all_embeddings = []
model = SentenceTransformer('all-MiniLM-L6-v2')
index = None


@app.route('/upload', methods=['POST'])
def upload_pdf():
    try:
        global all_chunks, all_embeddings, index, model

        pdf_file = request.files['file']
        filename = pdf_file.filename
        print(f"Received file: {filename}")

        # Create ./data if missing
        os.makedirs("data", exist_ok=True)

        path = os.path.join("data", filename)
        pdf_file.save(path)
        print(f"Saved file to: {path}")

        text = extract_text_from_pdf(path)
        print(f"Extracted text length: {len(text)}")

        chunks = chunk_text(text)
        embeddings = embed_chunks(chunks)

        all_chunks.extend(chunks)
        all_embeddings.extend(embeddings)

        index = build_vector_store(np.array(all_embeddings))

        return jsonify({"message": f"{filename} processed successfully!"})
    
    except Exception as e:
        print(f"[UPLOAD ERROR] {e}")
        return jsonify({"error": str(e)}), 500

@app.route('/ask', methods=['POST'])
def ask_question():
    global index, model, all_chunks

    question = request.json['question']
    if not index or not all_chunks:
        return jsonify({"answer": "No documents uploaded yet."}), 400

    top_chunks = search(index, question, model, all_chunks)
    answer = generate_answer(top_chunks, question)
    return jsonify({"answer": answer})

if __name__ == '__main__':
    app.run(debug=True, port=5050)
