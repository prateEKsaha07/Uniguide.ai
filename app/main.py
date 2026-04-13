import sys
import os
import json
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))



pdf_path = "data/raw/syllabus.pdf"
required_files = [
    "data/processed/faiss_index.bin",
    "data/processed/chunks.json"
]

def clear_old_data():
    files_to_delete = [
        "data/processed/faiss_index.bin",
        "data/processed/chunks.json",
        "data/processed/chunks_store.json",
        "data/processed/cleaned_text.txt"
    ]

    for file in files_to_delete:
        if os.path.exists(file):
            os.remove(file)
            print(f"🗑 Deleted: {file}")

def new_data_load():
        print("\n Processing new data...")

        from src.ingestion.extract import extract_text_from_pdf
        from src.ingestion.clean import clean_text
        from src.ingestion.chunk import chunk_by_units
        from src.embeddings.embedder import create_embeddings

        # Extract
        raw_text = extract_text_from_pdf(pdf_path)

        # Clean
        cleaned = clean_text(raw_text)

        with open("data/processed/cleaned_text.txt", "w", encoding="utf-8") as f:
            f.write(cleaned)

        # Chunk
        chunks = chunk_by_units(cleaned)

        with open("data/processed/chunks.json", "w", encoding="utf-8") as f:
            json.dump(chunks, f, indent=2)

        # Embeddings
        create_embeddings()

        print("New data loaded successfully!")


def setup_pipeline():
    while True:
        print("\n=== UniGuide AI Setup ===")
        print("1. Load new data")
        print("2. Use existing data")

        choice = input("Enter choice (1/2): ")

        if choice == "1":
            print("\nResetting old database (if exists)...")
            clear_old_data()

            print("\nLoading fresh data...")
            new_data_load()
            break
        elif choice == "2":
            print("\n Using existing vector database...")

            if not all(os.path.exists(f) for f in required_files):
                print("Missing data. Please load new data first.")
                continue
            else:
                break
        else:
            print("Invalid choice, try again.")


# starting the pipeline
print("Starting UniGuide AI...")
setup_pipeline()

from src.retrival.retriever import retrieve
from src.llm.llama3 import ask_llm

while True:
    query = input("Ask something: ")

    if query.lower() in ["exit", "quit"]:
        print("Exiting...")
        break

    results = retrieve(query,top_k=1)
    context = "\n\n".join(results)

    print("Context retrieved: ")
    print(context[:200])

    answer = ask_llm(context, query)
    print("Answer: ")
    print(answer)





