import sys
import os
import json
import re

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from src.ingestion.chunk import remove_irrelevant_sections, remove_subject_header

RAW_FILE = "data/raw/syllabus.txt"

REQUIRED_FILES = [
    "data/processed/faiss_index.bin",
    "data/processed/chunks.json"
]


def load_raw_text():
    with open(RAW_FILE, "r", encoding="utf-8") as f:
        return f.read()


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
            print(f" Deleted: {file}")

def new_data_load():
    print("\n Processing new data...")

    from src.ingestion.clean import clean_text
    from src.ingestion.chunk import (
        split_by_subject,
        split_intro_and_units,
        chunk_by_units,
        remove_irrelevant_sections,
        remove_subject_header
    )
    from src.embeddings.embedder import create_embeddings

    # 1. Load text
    raw = load_raw_text()

    # 2. Clean text
    cleaned = clean_text(raw)

    with open("data/processed/cleaned_text.txt", "w", encoding="utf-8") as f:
        f.write(cleaned)

    # 3. Split subjects
    subjects = split_by_subject(cleaned)

    all_chunks = []

    for subject in subjects:
        subject = remove_irrelevant_sections(subject)

        intro, unit_text = split_intro_and_units(subject)

        subject_name_match = re.search(r"Subject\s*:\s*(.*)", subject)
        subject_name = subject_name_match.group(1).strip() if subject_name_match else "Unknown"

    # COURSE INFO
        clean_intro = remove_subject_header(intro)
        all_chunks.append(f"[{subject_name}] COURSE INFO\n{clean_intro}")

    # UNITS
        unit_chunks = chunk_by_units(unit_text)

        for uc in unit_chunks:
            clean_uc = remove_subject_header(uc)
            all_chunks.append(f"[{subject_name}] {clean_uc}")

    # DEBUG
    print(f"\n Total chunks created: {len(all_chunks)}")

    # Save chunks
    with open("data/processed/chunks.json", "w", encoding="utf-8") as f:
        json.dump(all_chunks, f, indent=2)

    # 4. Create embeddings
    create_embeddings(all_chunks)

    print(" New data loaded successfully!")

def setup_pipeline():
    while True:
        print("\n=== UniGuide AI Setup ===")
        print("1. Load new data")
        print("2. Use existing data")

        choice = input("Enter choice (1/2): ")

        if choice == "1":
            print("\n Resetting old database...")
            clear_old_data()

            print("\n Loading fresh data...")
            new_data_load()
            break

        elif choice == "2":
            print("\n Using existing vector database...")

            if not all(os.path.exists(f) for f in REQUIRED_FILES):
                print(" Missing data. Please load new data first.")
                continue
            break

        else:
            print("Invalid choice, try again.")


print(" Starting UniGuide AI...")

setup_pipeline()

# Import AFTER setup (faster startup)
from src.ingestion.chunk import remove_irrelevant_sections, remove_subject_header
from src.retrival.retriever import retrieve
from src.llm.llama3 import ask_llm

while True:
    query = input("\nAsk something: ")

    if query.lower() in ["exit", "quit"]:
        print(" Exiting...")
        break

    results = retrieve(query, top_k=1)
    context = "\n\n".join(results)

    print("\n Context retrieved:")
    print(context[:200])

    answer = ask_llm(context, query)

    print("\n Answer:")
    print(answer)