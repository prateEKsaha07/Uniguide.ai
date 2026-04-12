import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.ingestion.extract import extract_text_from_pdf
from src.ingestion.clean import clean_text
from src.retrival.retriever import retrieve

pdf_path = "data/raw/syllabus.pdf"

# text = extract_text_from_pdf(pdf_path)
# cleaned_text = clean_text(text)

# with open("data/processed/cleaned_text.txt", "w", encoding="utf-8") as f:
#     f.write(cleaned_text)

# print("Text processing complete.")

query = "What is DBMS?"
results = retrieve(query)

for i,res in enumerate(results):
    print(f"Result {i+1}:\n{res[:200]}...")