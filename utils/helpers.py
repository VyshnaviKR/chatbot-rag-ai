from PyPDF2 import PdfReader

def load_text_file(path):
    with open(path, "r", encoding="utf-8") as f:
        return f.read()

def split_text(text, chunk_size=200):
    return [text[i:i+chunk_size] for i in range(0, len(text), chunk_size)]

def load_pdf(file):
    reader = PdfReader(file)
    text = ""
    for page in reader.pages:
        text += page.extract_text()
    return text