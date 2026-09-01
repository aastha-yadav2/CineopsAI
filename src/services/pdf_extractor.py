"""
CineOps AI - PDF Extraction Service
Standalone service layer for extracting plain text from screenplay PDF files.
Decoupled from analysis logic to support future PDF upload pipelines.
"""

import os
from typing import Union


class PDFExtractorService:
    """
    Service responsible for converting screenplay PDF documents into plain text.
    Decoupled from ScreenplayParserService.
    """

    def __init__(self):
        pass

    def extract_text_from_pdf_path(self, pdf_path: str) -> str:
        """
        Extract text content from a PDF file given its filesystem path.
        """
        if not os.path.exists(pdf_path):
            raise FileNotFoundError(f"PDF file not found at path: {pdf_path}")

        # Check if PyPDF or pypdf is available
        try:
            import pypdf
            reader = pypdf.PdfReader(pdf_path)
            extracted_text = []
            for page in reader.pages:
                text = page.extract_text()
                if text:
                    extracted_text.append(text)
            return "\n\n".join(extracted_text)
        except ImportError:
            # Fallback message / interface placeholder if pypdf is not yet installed
            raise NotImplementedError(
                "PDF extraction library (pypdf) is not currently installed. "
                "Please pass plain screenplay text directly or install pypdf."
            )

    def extract_text_from_pdf_bytes(self, pdf_bytes: bytes) -> str:
        """
        Extract text content from raw PDF byte stream.
        """
        if not pdf_bytes:
            raise ValueError("Empty PDF byte payload provided.")

        try:
            import io
            import pypdf
            reader = pypdf.PdfReader(io.BytesIO(pdf_bytes))
            extracted_text = [page.extract_text() for page in reader.pages if page.extract_text()]
            return "\n\n".join(extracted_text)
        except ImportError:
            raise NotImplementedError(
                "PDF extraction library (pypdf) is not currently installed. "
                "Please pass plain screenplay text directly or install pypdf."
            )
