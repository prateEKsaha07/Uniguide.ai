import numpy as np
import re

model = None
index = None
chunks = None


def load_resources():
    global model, index, chunks

    if model is None:
        print("Loading retriever resources...")

        from sentence_transformers import SentenceTransformer
        import faiss
        import json

        model = SentenceTransformer('all-MiniLM-L6-v2')

        index = faiss.read_index("data/processed/faiss_index.bin")

        with open("data/processed/chunks.json", "r", encoding="utf-8") as f:
            chunks = json.load(f)

        print("Retriever ready!")


word_to_num = {
    "one": "1",
    "two": "2",
    "three": "3",
    "four": "4",
    "five": "5"
}


def retrieve(query, top_k=2):
    load_resources()

    query_lower = query.lower()

    # Case 1: unit number (unit 1, unit 2 etc.)
    match = re.search(r'unit\s*(\d+)', query_lower)
    if match:
        unit_num = match.group(1)
        filtered = [c for c in chunks if f"unit {unit_num}:" in c.lower()]
        if filtered:
            return filtered

    # Case 2: word-based unit (unit one, unit two etc.)
    for word, num in word_to_num.items():
        if f"unit {word}" in query_lower:
            filtered = [c for c in chunks if f"unit {num}:" in c.lower()]
            if filtered:
                return filtered

    # Case 3: semantic search (FAISS)
    query_embedding = model.encode([query])
    query_embedding = np.array(query_embedding).astype('float32')

    distance, indices = index.search(query_embedding, top_k)

    results = [
        chunks[i]
        for i in indices[0]
        if i < len(chunks)
    ]

    return results