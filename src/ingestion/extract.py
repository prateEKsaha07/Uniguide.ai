def extract_text_from_pdf(pdf_path):
    try:
        import fitz  # PyMuPDF
    except ImportError:
        raise ImportError(" PyMuPDF not installed. Run: pip install pymupdf")

    try:
        doc = fitz.open(pdf_path)
    except Exception as e:
        raise RuntimeError(f" Failed to open PDF: {e}")

    full_text = ""

    for page in doc:
        try:
            text = page.get_text()
            if text:
                full_text += text + "\n"
        except Exception:
            continue 

    if not full_text.strip():
        raise ValueError(" No readable text found in PDF (likely scanned or encoded)")

    return full_text