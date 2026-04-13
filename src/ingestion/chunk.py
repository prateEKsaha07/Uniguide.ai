import json
import re
def chunk_by_units(text):
    # Match "Unit 1:" with anything after it
    pattern = r'(Unit\s+\d+:[\s\S]*?)(?=Unit\s+\d+:|$)'
    
    chunks = re.findall(pattern, text)
    
    return [chunk.strip() for chunk in chunks]

if __name__ == "__main__":
    with open("data/processed/cleaned_text.txt", "r", encoding="utf-8") as f:
        text = f.read()

    chunks = chunk_by_units(text)

    with open("data/processed/chunks.json", "w", encoding="utf-8") as f:
        json.dump(chunks, f, indent=2)

    print(f"Created {len(chunks)} chunks")
