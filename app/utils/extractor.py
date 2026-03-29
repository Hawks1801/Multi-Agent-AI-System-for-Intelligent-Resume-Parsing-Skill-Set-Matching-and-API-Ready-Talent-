import os
import pdfplumber
import docx
from typing import Optional

class DocumentExtractor:
    @staticmethod
    def extract_from_pdf(file_path: str) -> str:
        """Extracts text from a PDF file while preserving some layout."""
        text = ""
        with pdfplumber.open(file_path) as pdf:
            for page in pdf.pages:
                page_text = page.extract_text(layout=True)
                if page_text:
                    text += page_text + "\n"
        return text

    @staticmethod
    def extract_from_docx(file_path: str) -> str:
        """Extracts text from a DOCX file."""
        doc = docx.Document(file_path)
        full_text = []
        for para in doc.paragraphs:
            full_text.append(para.text)
        return "\n".join(full_text)

    @staticmethod
    def extract_from_text(file_path: str) -> str:
        """Reads text from a plain text file."""
        with open(file_path, 'r', encoding='utf-8') as f:
            return f.read()

    @classmethod
    def extract_text(cls, file_path: str) -> Optional[str]:
        """Generic method to extract text based on file extension."""
        ext = os.path.splitext(file_path)[1].lower()
        if ext == '.pdf':
            return cls.extract_from_pdf(file_path)
        elif ext == '.docx':
            return cls.extract_from_docx(file_path)
        elif ext in ['.txt', '.md']:
            return cls.extract_from_text(file_path)
        else:
            raise ValueError(f"Unsupported file format: {ext}")
