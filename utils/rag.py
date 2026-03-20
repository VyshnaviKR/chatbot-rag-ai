from models.embeddings import embed
from utils.helpers import load_text_file, split_text, load_pdf
import numpy as np

documents = []
vectors = []

def load_data():
    text = load_text_file("data/sample.txt")
    chunks = split_text(text)

    for chunk in chunks:
        documents.append(chunk)
        vectors.append(embed(chunk))

def load_uploaded_file(file):
    text = load_pdf(file)
    chunks = split_text(text)

    for chunk in chunks:
        documents.append(chunk)
        vectors.append(embed(chunk))

def retrieve(query):
    if not documents:
        return None

    query_vec = embed(query)
    scores = [np.dot(query_vec, v) for v in vectors]

    return documents[int(np.argmax(scores))]