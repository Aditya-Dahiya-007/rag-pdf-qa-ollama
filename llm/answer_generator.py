import subprocess

def generate_answer(context_chunks, question):
    context = "\n\n".join(context_chunks)
    prompt = f"Use the following context to answer the question:\n\n{context}\n\nQuestion: {question}\nAnswer:"
    result = subprocess.run(
        ["ollama", "run", "llama3"],
        input=prompt.encode(),
        stdout=subprocess.PIPE
    )
    return result.stdout.decode()
