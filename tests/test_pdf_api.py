"""
CineOps AI - PDF Extraction & API Unit Tests
Tests for PDFExtractorService, POST /api/analyze-pdf endpoint, file size validation,
MIME type validation, corrupt file handling, and mock pipeline integration.
"""

import io
from fastapi.testclient import TestClient
from src.api.main import app
from src.services.pdf_extractor import PDFExtractorService

client = TestClient(app)

# Minimal valid PDF byte payload containing extractable screenplay text stream
VALID_SCREENPLAY_PDF_BYTES = (
    b"%PDF-1.4\n"
    b"1 0 obj\n<< /Type /Catalog /Pages 2 0 R >>\nendobj\n"
    b"2 0 obj\n<< /Type /Pages /Kids [3 0 R] /Count 1 >>\nendobj\n"
    b"3 0 obj\n<< /Type /Page /Parent 2 0 R /Resources << /Font << /F1 4 0 R >> >> /MediaBox [0 0 612 792] /Contents 5 0 R >>\nendobj\n"
    b"4 0 obj\n<< /Type /Font /Subtype /Type1 /BaseFont /Helvetica >>\nendobj\n"
    b"5 0 obj\n<< /Length 95 >>\nstream\n"
    b"BT\n/F1 12 Tf\n100 700 Td\n(INT. POLICE PRECINCT - OFFICE - NIGHT) Tj\n0 -20 Td\n(Detective Miller inspects tablet computer.) Tj\nET\n"
    b"endstream\nendobj\n"
    b"xref\n0 6\n0000000000 65535 f \n0000000009 00000 n \n0000000058 00000 n \n0000000115 00000 n \n0000000234 00000 n \n0000000305 00000 n \n"
    b"trailer\n<< /Size 6 /Root 1 0 R >>\n"
    b"startxref\n450\n%%EOF\n"
)


def test_pdf_extractor_service_extracts_text():
    """Test PDFExtractorService extracts readable screenplay text from valid PDF bytes."""
    service = PDFExtractorService()
    text = service.extract_text_from_pdf_bytes(VALID_SCREENPLAY_PDF_BYTES)
    assert text is not None
    assert "INT. POLICE PRECINCT" in text
    assert "Miller inspects tablet" in text


def test_analyze_pdf_endpoint_valid_flow():
    """Test POST /api/analyze-pdf ingests screenplay PDF and returns ProductionPlan in mock mode."""
    files = {"file": ("screenplay.pdf", io.BytesIO(VALID_SCREENPLAY_PDF_BYTES), "application/pdf")}
    data = {"mock_mode": "true"}

    response = client.post("/api/analyze-pdf", files=files, data=data)
    assert response.status_code == 200, response.text
    result = response.json()
    assert "total_estimated_days" in result
    assert "scene_groupings" in result
    assert "shooting_schedule" in result
    assert len(result["scene_groupings"]) > 0


def test_analyze_pdf_endpoint_invalid_extension():
    """Test POST /api/analyze-pdf rejects files without .pdf extension."""
    files = {"file": ("script.txt", io.BytesIO(b"Plain text screenplay"), "text/plain")}
    response = client.post("/api/analyze-pdf", files=files)
    assert response.status_code == 400
    assert "Uploaded file must be a PDF document" in response.json()["detail"]


def test_analyze_pdf_endpoint_invalid_mime_type():
    """Test POST /api/analyze-pdf rejects invalid MIME types."""
    files = {"file": ("script.pdf", io.BytesIO(b"Fake PNG content"), "image/png")}
    response = client.post("/api/analyze-pdf", files=files)
    assert response.status_code == 400
    assert "Invalid MIME type" in response.json()["detail"]


def test_analyze_pdf_endpoint_corrupt_pdf():
    """Test POST /api/analyze-pdf rejects corrupt/unparseable PDF content."""
    files = {"file": ("script.pdf", io.BytesIO(b"Not a valid pdf structure"), "application/pdf")}
    response = client.post("/api/analyze-pdf", files=files)
    assert response.status_code == 400
    assert "Could not extract readable" in response.json()["detail"]


def test_analyze_pdf_endpoint_file_too_large():
    """Test POST /api/analyze-pdf enforces 10MB file size limit."""
    oversized_bytes = b"%PDF-1.4\n" + b"X" * (11 * 1024 * 1024)
    files = {"file": ("huge_script.pdf", io.BytesIO(oversized_bytes), "application/pdf")}
    response = client.post("/api/analyze-pdf", files=files)
    assert response.status_code == 400
    assert "10MB limit" in response.json()["detail"]
