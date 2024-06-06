import fitz  # PyMuPDF
import os

def extract_text_from_pdf(pdf_path):
    doc = fitz.open(pdf_path)
    text = ""
    for page in doc:
        text += page.get_text()
    return text

def extract_text_from_all_pdfs(directory):
    documents = {}
    for filename in os.listdir(directory):
        if filename.endswith(".pdf"):
            file_path = os.path.join(directory, filename)
            text = extract_text_from_pdf(file_path)
            documents[filename] = text
    return documents

if __name__ == "__main__":
    directory = "./documents"
    documents = extract_text_from_all_pdfs(directory)
    for title, content in documents.items():
        print(f"Title: {title}\nContent: {content[:500]}...\n")
