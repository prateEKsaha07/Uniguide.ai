import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.ingestion.extract import extract_text_from_pdf
from src.ingestion.clean import clean_text
from src.retrival.retriever import retrieve
from src.llm.llama3 import ask_llm

pdf_path = "data/raw/syllabus.pdf"

# text = extract_text_from_pdf(pdf_path)
# cleaned_text = clean_text(text)

# with open("data/processed/cleaned_text.txt", "w", encoding="utf-8") as f:
#     f.write(cleaned_text)

# print("Text processing complete.")

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





