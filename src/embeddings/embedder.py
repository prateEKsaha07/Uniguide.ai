from sentence_transformers import SentenceTransformer
import json
import faiss
import numpy as np

load_model = SentenceTransformer('all-MiniLM-L6-v2') # Load the model once

def create_embeddings():
    # loading the chnks from the json file
    with open("data/processed/chunks.json", "r", encoding="utf-8") as f:
        chunks = json.load(f)

    # creating the embeddings for the chunks
    embeddings = load_model.encode(chunks)

    embaddings = np.array(embeddings).astype('float32')

    # faiss index
    dimension = embeddings.shape[1]
    index = faiss.IndexFlatL2(dimension)

    index.add(embeddings)

    # saving the index
    faiss.write_index(index, "data/processed/faiss_index.bin")

    with open("data/processed/chunks_store.json", "w", encoding="utf-8") as f:
        json.dump(chunks, f, indent=2)

    print("Embeddings created and index saved.")


if __name__ == "__main__":
    create_embeddings()



     