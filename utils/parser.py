import io
import fitz  # pymupdf
from docx import Document


def parse_pdf(file) -> str:
    """Extract text from a PDF file object."""
    file_bytes = file.read()
    doc = fitz.open(stream=file_bytes, filetype="pdf")
    text = ""
    for page in doc:
        text += page.get_text()
    doc.close()
    return text.strip()


def parse_docx(file) -> str:
    """Extract text from a DOCX file object."""
    file_bytes = io.BytesIO(file.read())
    doc = Document(file_bytes)
    paragraphs = [p.text for p in doc.paragraphs if p.text.strip()]
    return "\n".join(paragraphs).strip()


def chunk_text(text: str, chunk_size: int = 400, overlap: int = 50) -> list[str]:
    """Split text into overlapping chunks by word count."""
    words = text.split()
    chunks = []
    for i in range(0, len(words), chunk_size - overlap):
        chunk = " ".join(words[i: i + chunk_size])
        if chunk:
            chunks.append(chunk)
    return chunks
