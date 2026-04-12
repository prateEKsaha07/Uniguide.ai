import faiss
import json 
import numpy as np
from sentence_transformers import SentenceTransformer

model = SentenceTransformer('all-MiniLM-L6-v2')
index = faiss.read_index("data/processed/faiss_index.bin")
with open("data/processed/chunks_store.json", "r", encoding="utf-8") as f:
    chunks = json.load(f)

def retrieve(query, top_k=2):
    query_embedding = model.encode([query])
    query_embedding = np.array(query_embedding).astype('float32')

    ditance, indices = index.search(query_embedding, top_k)
    results = [chunks[i] for i in indices[0]]
    return results


