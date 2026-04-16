import re


def clean_text(text):
    # normalize line breaks
    text = re.sub(r'\r\n', '\n', text)

    # remove extra blank lines but KEEP structure
    text = re.sub(r'\n+', '\n', text)

    # fix UNIT formats
    text = re.sub(r'UNIT\s*[-–]\s*I', 'UNIT I', text, flags=re.IGNORECASE)
    text = re.sub(r'UNIT\s*[-–]\s*II', 'UNIT II', text, flags=re.IGNORECASE)
    text = re.sub(r'UNIT\s*[-–]\s*III', 'UNIT III', text, flags=re.IGNORECASE)
    text = re.sub(r'UNIT\s*[-–]\s*IV', 'UNIT IV', text, flags=re.IGNORECASE)
    text = re.sub(r'UNIT\s*[-–]\s*V', 'UNIT V', text, flags=re.IGNORECASE)

    # clean spaces inside lines only
    text = re.sub(r'[ \t]+', ' ', text)

    return text.strip()