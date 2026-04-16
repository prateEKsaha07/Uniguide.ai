import json
import re


def remove_irrelevant_sections(text):
    text = re.split(r'Text Books:', text, flags=re.IGNORECASE)[0]
    text = re.split(r'Reference Books:', text, flags=re.IGNORECASE)[0]
    return text.strip()

def remove_subject_header(text):
    return re.sub(r"Subject\s*:\s*.*?\n", "", text, flags=re.IGNORECASE).strip()


def split_by_subject(text):
    subjects = re.split(r'\n\s*Subject\s*:', text, flags=re.IGNORECASE)

    cleaned = []
    for s in subjects:
        s = s.strip()

        # ignore garbage header
        if not s or "University" in s[:100]:
            continue

        cleaned.append("Subject :" + s)

    return cleaned


def split_intro_and_units(text):
    match = re.search(r"UNIT\s+[IVX0-9]+", text, re.IGNORECASE)

    if match:
        idx = match.start()
        intro = text[:idx]
        units = text[idx:]
    else:
        intro = text
        units = ""

    return intro.strip(), units.strip()


def remove_subject_header(text):
    return re.sub(r"Subject\s*:.*?\n", "", text, flags=re.IGNORECASE)

def remove_irrelevant_sections(text):
    text = re.split(r'Text Books:', text, flags=re.IGNORECASE)[0]
    return text.strip()

def chunk_by_units(text):
    chunks = re.split(r'(UNIT\s+[IVX0-9]+.*)', text, flags=re.IGNORECASE)

    final_chunks = []
    current = ""

    for part in chunks:
        if re.match(r'UNIT\s+[IVX0-9]+', part, re.IGNORECASE):
            if current:
                final_chunks.append(current.strip())
            current = part
        else:
            current += part

    if current:
        final_chunks.append(current.strip())

    print(f" Unit chunks created: {len(final_chunks)}")
    return final_chunks


if __name__ == "__main__":
    with open("data/processed/cleaned_text.txt", "r", encoding="utf-8") as f:
        text = f.read()

    subjects = split_by_subject(text)

    all_chunks = []

    for subject in subjects:
        subject = remove_irrelevant_sections(subject)

        intro, unit_text = split_intro_and_units(subject)

        subject_name_match = re.search(r"Subject\s*:\s*(.*)", subject)
        subject_name = subject_name_match.group(1).strip() if subject_name_match else "Unknown"

        # intro
        clean_intro = remove_subject_header(intro)
        all_chunks.append(f"[{subject_name}] COURSE INFO\n{clean_intro}")

        # units
        unit_chunks = chunk_by_units(unit_text)

        for uc in unit_chunks:
            clean_uc = remove_subject_header(uc)
            all_chunks.append(f"[{subject_name}] {clean_uc}")

    with open("data/processed/chunks.json", "w", encoding="utf-8") as f:
        json.dump(all_chunks, f, indent=2)

    print(f"\nTotal chunks created: {len(all_chunks)}")