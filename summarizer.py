from sumy.parsers.plaintext import PlaintextParser
from sumy.nlp.tokenizers import Tokenizer
from sumy.summarizers.lsa import LsaSummarizer
import PyPDF2
from docx import Document

def summarize_document(file_path):
    if file_path.endswith('.pdf'):
        content = extract_pdf_content(file_path)
    elif file_path.endswith('.txt'):
        content = extract_txt_content(file_path)
    elif file_path.endswith('.docx'):
        content = extract_docx_content(file_path)
    else:
        raise ValueError("Unsupported file format. Please provide a .pdf, .txt, or .docx file.")

    parser = PlaintextParser.from_string(content, Tokenizer("english"))
    summarizer = LsaSummarizer()
    summary = summarizer(parser.document, 3)  # Summarize to 3 sentences
    
    summary_text = " ".join([str(sentence) for sentence in summary])
    return summary_text

def extract_pdf_content(file_path):
    text = ""
    with open(file_path, 'rb') as file:
        reader = PyPDF2.PdfReader(file)
        for page in reader.pages:
            text += page.extract_text() or ""  # Handle pages with no text
    return text

def extract_txt_content(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        content = file.read()
    return content

def extract_docx_content(file_path):
    doc = Document(file_path)
    text = "\n".join([para.text for para in doc.paragraphs])
    return text
