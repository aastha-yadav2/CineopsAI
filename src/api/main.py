"""
CineOps AI - FastAPI Backend Application
Exposes REST API endpoints for screenplay analysis, Parallel web research,
and autonomous film production planning.
"""

import os
import sys
from pathlib import Path
from typing import List, Optional

# Ensure root directory is on sys.path
ROOT_DIR = Path(__file__).resolve().parent.parent.parent
if str(ROOT_DIR) not in sys.path:
    sys.path.insert(0, str(ROOT_DIR))

from dotenv import load_dotenv
from fastapi import FastAPI, File, Form, HTTPException, UploadFile, status
from fastapi.middleware.cors import CORSMiddleware

from src.api.schemas import (
    CombinedAnalyzeRequest,
    GeneratePlanRequest,
    HealthResponse,
    ScreenplayAnalyzeRequest,
)
from src.models.planner import ProductionPlan
from src.models.production import ScreenplayProductionAnalysis
from src.services.pdf_extractor import PDFExtractorService
from src.services.parallel_search import ParallelSearchService
from src.services.production_planner_service import ProductionPlannerService
from src.services.screenplay_parser import ScreenplayParserService

# Load environment configuration
load_dotenv()

# Initialize FastAPI App
app = FastAPI(
    title="CineOps AI API",
    version="1.0.0",
    description="Autonomous Film Production Assistant API powering Screenplay Analysis, Parallel Research, and Production Planning.",
)

# Configure CORS origins from environment or default local development origins
raw_origins = os.getenv("CINEOPS_CORS_ORIGINS")
if raw_origins and raw_origins.strip():
    allowed_origins = [origin.strip() for origin in raw_origins.split(",") if origin.strip()]
else:
    allowed_origins = [
        "http://localhost:3000",
        "http://localhost:5173",
        "http://127.0.0.1:3000",
        "http://127.0.0.1:5173",
    ]

app.add_middleware(
    CORSMiddleware,
    allow_origins=allowed_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/health", response_model=HealthResponse, status_code=status.HTTP_200_OK)
def health_check():
    """Health status check endpoint."""
    return HealthResponse(status="ok", service="cineops-ai")


@app.post(
    "/api/analyze-screenplay",
    response_model=ScreenplayProductionAnalysis,
    status_code=status.HTTP_200_OK,
)
def analyze_screenplay(req: ScreenplayAnalyzeRequest):
    """
    Extract structured 11-parameter production breakdown from screenplay text.
    Reuses ScreenplayParserService without duplicating business logic.
    """
    try:
        parser = ScreenplayParserService()
        analysis = parser.analyze_script_text(req.script_text, mock_mode=req.mock_mode)
        return analysis
    except Exception as err:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Screenplay analysis failed: {str(err)}",
        ) from err


@app.post(
    "/api/generate-plan",
    response_model=ProductionPlan,
    status_code=status.HTTP_200_OK,
)
def generate_production_plan(req: GeneratePlanRequest):
    """
    Synthesize structured screenplay analysis and optional research into an actionable production plan.
    Reuses ProductionPlannerService.
    """
    try:
        planner = ProductionPlannerService()
        plan = planner.generate_plan(
            analysis=req.analysis,
            research_data=req.research_data,
            mock_mode=req.mock_mode,
        )
        return plan
    except Exception as err:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Production plan generation failed: {str(err)}",
        ) from err


@app.post(
    "/api/analyze",
    response_model=ProductionPlan,
    status_code=status.HTTP_200_OK,
)
def combined_analyze_pipeline(req: CombinedAnalyzeRequest):
    """
    Execute full end-to-end CineOps pipeline:
    Screenplay Text -> Screenplay Analyst -> Parallel Research -> Production Planner -> ProductionPlan.
    """
    try:
        # Determine effective mock mode
        if req.mock_mode is None:
            mock_mode = os.getenv("CINEOPS_MOCK_MODE", "1") == "1"
        else:
            mock_mode = req.mock_mode

        # 1. Screenplay Analysis
        parser = ScreenplayParserService()
        analysis = parser.analyze_script_text(req.script_text, mock_mode=mock_mode)

        # 2. Parallel Research
        research_data = None
        if not mock_mode:
            parallel_key = os.getenv("PARALLEL_API_KEY")
            if parallel_key and parallel_key.strip():
                search_service = ParallelSearchService(api_key=parallel_key)
                objective = (
                    req.research_objective
                    or "Find film set safety regulations for outdoor night wet-down rain scenes and drone permits."
                )
                queries = req.research_queries or [
                    "film set rain machine safety guidelines",
                    "outdoor night shoot wet down electrical safety",
                ]
                research_data = search_service.search(objective=objective, search_queries=queries)

        # 3. Production Planning
        planner = ProductionPlannerService()
        plan = planner.generate_plan(
            analysis=analysis,
            research_data=research_data,
            mock_mode=mock_mode,
        )
        return plan

    except Exception as err:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"CineOps pipeline execution failed: {str(err)}",
        ) from err


@app.post(
    "/api/analyze-pdf",
    response_model=ProductionPlan,
    status_code=status.HTTP_200_OK,
)
async def analyze_pdf_pipeline(
    file: UploadFile = File(...),
    mock_mode: Optional[bool] = Form(None),
):
    """
    Ingest a screenplay PDF file, extract text via PDFExtractorService,
    and execute the complete CineOps production analysis & planning pipeline.
    """
    filename = file.filename or ""

    # 1. Validate file extension
    if not filename.lower().endswith(".pdf"):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Uploaded file must be a PDF document (.pdf).",
        )

    # 2. Validate MIME type sensibly
    valid_mimes = [
        "application/pdf",
        "application/x-pdf",
        "application/octet-stream",
        "application/vnd.pdf",
    ]
    if file.content_type and file.content_type.lower() not in valid_mimes:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Invalid MIME type '{file.content_type}'. Uploaded file must be a PDF document.",
        )

    # 3. Read uploaded bytes & enforce 10MB size limit
    pdf_bytes = await file.read()
    max_bytes = 10 * 1024 * 1024  # 10 MB

    if len(pdf_bytes) > max_bytes:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="PDF file size exceeds the 10MB limit.",
        )

    if not pdf_bytes or len(pdf_bytes) == 0:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Uploaded PDF file is empty (0 bytes).",
        )

    # 4. Extract plain text using PDFExtractorService
    pdf_service = PDFExtractorService()
    try:
        extracted_text = pdf_service.extract_text_from_pdf_bytes(pdf_bytes)
    except Exception as err:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Could not extract readable text from PDF: {str(err)}",
        ) from err

    if not extracted_text or len(extracted_text.strip()) < 10:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Could not extract readable screenplay text from PDF. The PDF may be empty, image-only, or corrupted.",
        )

    # 5. Execute CineOps Analysis & Planning Pipeline
    try:
        if mock_mode is None:
            effective_mock = os.getenv("CINEOPS_MOCK_MODE", "1") == "1"
        else:
            effective_mock = mock_mode

        parser = ScreenplayParserService()
        analysis = parser.analyze_script_text(extracted_text, mock_mode=effective_mock)

        research_data = None
        if not effective_mock:
            parallel_key = os.getenv("PARALLEL_API_KEY")
            if parallel_key and parallel_key.strip():
                search_service = ParallelSearchService(api_key=parallel_key)
                objective = "Find film set safety regulations for outdoor night wet-down rain scenes and drone permits."
                queries = [
                    "film set rain machine safety guidelines",
                    "outdoor night shoot wet down electrical safety",
                ]
                research_data = search_service.search(objective=objective, search_queries=queries)

        planner = ProductionPlannerService()
        plan = planner.generate_plan(
            analysis=analysis,
            research_data=research_data,
            mock_mode=effective_mock,
        )
        return plan

    except Exception as err:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Pipeline error processing PDF screenplay: {str(err)}",
        ) from err



# Mount static directory for single-page web dashboard if directory exists
static_dir = ROOT_DIR / "static"
if static_dir.exists():
    from fastapi.staticfiles import StaticFiles
    app.mount("/", StaticFiles(directory=str(static_dir), html=True), name="static")

