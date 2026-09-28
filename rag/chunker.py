def chunk_text(text, chunk_size=700, overlap=120):
    if chunk_size <= 0 or overlap < 0 or overlap >= chunk_size:
        raise ValueError("chunk_size must be positive and overlap must be smaller than chunk_size")
    text = " ".join(text.split())
    chunks = []
    start = 0
    while start < len(text):
        end = min(start + chunk_size, len(text))
        piece = text[start:end].strip()
        if piece:
            chunks.append(piece)
        if end >= len(text):
            break
        start = end - overlap
    return chunks


def chunk_documents(documents, chunk_size=700, overlap=120):
    result = []
    for doc in documents:
        for i, chunk in enumerate(chunk_text(doc["text"], chunk_size, overlap), start=1):
            result.append({"source": doc["source"], "chunk_id": i, "text": chunk})
    return result
