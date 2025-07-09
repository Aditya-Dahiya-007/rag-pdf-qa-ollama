def search(index, query, model, chunks, top_k=5):
    query_vec = model.encode([query])
    D, I = index.search(query_vec, top_k)
    return [chunks[i] for i in I[0]]
