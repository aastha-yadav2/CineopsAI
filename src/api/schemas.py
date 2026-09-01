"""
CineOps AI - API Request & Response Schemas
Pydantic models for REST API endpoint payloads.
"""

from typing import List, Optional
from pydantic import BaseModel, Field

from src.models.planner import ProductionPlan
from src.models.production import ScreenplayProductionAnalysis
from src.services.parallel_search import ProductionResearchResponse


class HealthResponse(BaseModel):
    """Response schema for GET /health endpoint."""
    status: str = Field(default="ok", description="Service health status")
    service: str = Field(default="cineops-ai", description="Service identifier")


class ScreenplayAnalyzeRequest(BaseModel):
    """Request payload for POST /api/analyze-screenplay endpoint."""
    script_text: str = Field(..., min_length=10, description="Raw screenplay text content")
    mock_mode: Optional[bool] = Field(
        default=None,
        description="Override mock execution mode. Defaults to environment setting CINEOPS_MOCK_MODE."
    )


class GeneratePlanRequest(BaseModel):
    """Request payload for POST /api/generate-plan endpoint."""
    analysis: ScreenplayProductionAnalysis = Field(..., description="Structured screenplay production analysis")
    research_data: Optional[ProductionResearchResponse] = Field(
        default=None,
        description="Optional Parallel web research response"
    )
    mock_mode: Optional[bool] = Field(
        default=None,
        description="Override mock execution mode. Defaults to environment setting CINEOPS_MOCK_MODE."
    )


class CombinedAnalyzeRequest(BaseModel):
    """Request payload for POST /api/analyze combined pipeline endpoint."""
    script_text: str = Field(..., min_length=10, description="Raw screenplay text content")
    research_objective: Optional[str] = Field(
        default=None,
        description="Custom research goal for Parallel Search (optional)"
    )
    research_queries: Optional[List[str]] = Field(
        default=None,
        description="Explicit research keyword queries for Parallel Search (optional)"
    )
    mock_mode: Optional[bool] = Field(
        default=None,
        description="Override mock execution mode. Defaults to environment setting CINEOPS_MOCK_MODE."
    )
