import json
import re

def chunk_by_units(text):
    # Match "Unit 1:" with anything after it
    pattern = r'(Unit\s+\d+:[\s\S]*?)(?=Unit\s+\d+:|$)'
    
    chunks = re.findall(pattern, text)
    
    return [chunk.strip() for chunk in chunks]


# def chunk_text(text, chunk_size=120, overlap=30):
#     words = text.split()
#     chunks = []

#     start = 0 
#     while start < len(words):
#         end = start + chunk_size
#         chunk = words[start:end]

#         chunks.append(" ".join(chunk))
#         start = end - overlap #it will move with the chunk size but will overlap with the previous chunk by the specified overlap

#     return chunks



if __name__ == "__main__":
    with open("data/processed/cleaned_text.txt", "r", encoding="utf-8") as f:
        text = f.read()

    chunks = chunk_by_units(text)

    with open("data/processed/chunks.json", "w", encoding="utf-8") as f:
        json.dump(chunks, f, indent=2)

    print(f"Created {len(chunks)} chunks")


# if __name__ == "__main__":
#     with open("data/processed/cleaned_text.txt", "r", encoding="utf-8") as f:
#         cleaned_text = f.read()

#     chunks = chunk_text(cleaned_text)

#     with open("data/processed/chunks.json", "w", encoding="utf-8") as f:
#         json.dump(chunks, f, ensure_ascii=False, indent=4)

#     print(f"Created {len(chunks)} chunks.")