import json
import numpy as np

model = None


def create_embeddings(chunks=None):
    global model

    if model is None:
        print(" Loading embedding model...")
        from sentence_transformers import SentenceTransformer
        model = SentenceTransformer('all-MiniLM-L6-v2')

    import faiss


    if chunks is None:
        print(" Loading chunks from file...")
        with open("data/processed/chunks.json", "r", encoding="utf-8") as f:
            chunks = json.load(f)

    if not chunks:
        raise ValueError(" No chunks available for embedding")

    print(" Creating embeddings...")
    embeddings = model.encode(chunks, batch_size=8)

    embeddings = np.array(embeddings).astype('float32')

    dimension = embeddings.shape[1]
    index = faiss.IndexFlatL2(dimension)

    index.add(embeddings)

    faiss.write_index(index, "data/processed/faiss_index.bin")

    with open("data/processed/chunks.json", "w", encoding="utf-8") as f:
        json.dump(chunks, f, indent=2)

    print(" Embeddings created and index saved.")


if __name__ == "__main__":
    create_embeddings()