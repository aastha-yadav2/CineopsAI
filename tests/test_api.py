"""
CineOps AI - FastAPI Endpoint Unit Tests
Tests for health check, screenplay analysis, plan generation, and combined pipeline endpoints
using FastAPI TestClient with zero external network calls.
"""

from fastapi.testclient import TestClient
from src.api.main import app

client = TestClient(app)


def test_health_endpoint():
    """Test GET /health returns status ok and service name."""
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "ok", "service": "cineops-ai"}


def test_analyze_screenplay_endpoint():
    """Test POST /api/analyze-screenplay parses script text into structured analysis."""
    sample_text = (
        "INT. POLICE PRECINCT - OFFICE - NIGHT\n\n"
        "Detective Miller inspects tablet computer while rain splashes outside."
    )
    response = client.post(
        "/api/analyze-screenplay",
        json={"script_text": sample_text, "mock_mode": True},
    )

    assert response.status_code == 200
    data = response.json()
    assert "total_scenes" in data
    assert "scenes" in data
    assert len(data["scenes"]) > 0


def test_generate_plan_endpoint():
    """Test POST /api/generate-plan generates production plan from structured analysis."""
    # Obtain structured analysis first
    sample_text = "EXT. ABANDONED ALLEYWAY - NIGHT\nHeavy rain falls on wet pavement."
    analysis_resp = client.post(
        "/api/analyze-screenplay",
        json={"script_text": sample_text, "mock_mode": True},
    )
    analysis_data = analysis_resp.json()

    # Generate plan
    plan_resp = client.post(
        "/api/generate-plan",
        json={"analysis": analysis_data, "mock_mode": True},
    )

    assert plan_resp.status_code == 200
    plan_data = plan_resp.json()
    assert "total_estimated_days" in plan_data
    assert "scene_groupings" in plan_data
    assert "shooting_schedule" in plan_data


def test_combined_analyze_endpoint():
    """Test POST /api/analyze executes full pipeline end-to-end."""
    sample_text = (
        "SCENARIO TITLE: NIGHTFALL\n\n"
        "EXT. WAREHOUSE ROOFTOP - DAWN\n\n"
        "High wind sweeps across the roof as Suspect X pulls out a smoke grenade."
    )
    response = client.post(
        "/api/analyze",
        json={
            "script_text": sample_text,
            "research_objective": "Test rooftop drone rules",
            "mock_mode": True,
        },
    )

    assert response.status_code == 200
    plan_data = response.json()
    assert "total_estimated_days" in plan_data
    assert "resource_requirements" in plan_data
    assert "production_risks" in plan_data
    assert "research_references" in plan_data


def test_invalid_request_validation():
    """Test Pydantic validation returns HTTP 422 for script_text under minimum length."""
    response = client.post(
        "/api/analyze-screenplay",
        json={"script_text": "too short"},
    )
    assert response.status_code == 422
