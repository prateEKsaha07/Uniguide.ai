import numpy as np
import re

model = None
index = None
chunks = None


def extract_subject(query):
    q = query.lower()

    if "java" in q:
        return "java"
    if "dbms" in q:
        return "dbms"
    if "operating system" in q or "os" in q:
        return "operating systems"

    return None


def load_resources():
    global model, index, chunks

    if model is None:
        print(" Loading retriever resources...")

        from sentence_transformers import SentenceTransformer
        import faiss
        import json

        model = SentenceTransformer('all-MiniLM-L6-v2')
        index = faiss.read_index("data/processed/faiss_index.bin")

        with open("data/processed/chunks.json", "r", encoding="utf-8") as f:
            chunks = json.load(f)

        print(" Retriever ready!")


word_to_num = {
    "one": "1",
    "two": "2",
    "three": "3",
    "four": "4",
    "five": "5"
}

num_to_roman = {
    "1": "I",
    "2": "II",
    "3": "III",
    "4": "IV",
    "5": "V"
}


def retrieve(query, top_k=2):
    load_resources()

    if not chunks:
        raise ValueError(" No chunks found. Run data loading first.")

    query_lower = query.lower()

    subject = extract_subject(query)

    filtered_chunks = chunks

    if subject:
        filtered_chunks = [c for c in chunks if subject in c.lower()]
        print(f" Subject detected: {subject}")

    # numeric: unit 1
    match = re.search(r'unit\s*(\d+)', query_lower)
    if match:
        num = match.group(1)
        roman = num_to_roman.get(num)

        if roman:
            result = [c for c in filtered_chunks if f"UNIT {roman}" in c.upper()]
            if result:
                print(f" Unit detected: {roman}")
                return result

    # word: unit one
    for word, num in word_to_num.items():
        if f"unit {word}" in query_lower:
            roman = num_to_roman.get(num)
            result = [c for c in filtered_chunks if f"UNIT {roman}" in c.upper()]
            if result:
                print(f" Unit detected: {roman}")
                return result

    # roman: unit i
    match = re.search(r'unit\s*([ivx]+)', query_lower)
    if match:
        roman = match.group(1).upper()
        result = [c for c in filtered_chunks if f"UNIT {roman}" in c.upper()]
        if result:
            print(f" Unit detected: {roman}")
            return result

    print(" Using semantic search...")

    query_embedding = model.encode([query])
    query_embedding = np.array(query_embedding).astype('float32')

    distance, indices = index.search(query_embedding, top_k)

    results = [
        filtered_chunks[i]
        for i in indices[0]
        if i < len(filtered_chunks)
    ]

    return results