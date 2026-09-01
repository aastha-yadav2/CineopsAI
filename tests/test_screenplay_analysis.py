"""
CineOps AI - Screenplay Analysis Test Suite
Tests for Pydantic production breakdown models, ScreenplayParserService, PDFExtractorService,
and ADK Agent model configuration.
"""

import os
import pytest
from src.agents.screenplay_agent import screenplay_agent
from src.models.production import ScreenplayProductionAnalysis
from src.models.screenplay import (
    SceneAnalysis,
    SceneLocationType,
    TimeOfDay,
    ProductionDependency,
    ProductionRisk,
)
from src.services.pdf_extractor import PDFExtractorService
from src.services.screenplay_parser import ScreenplayParserService


@pytest.fixture
def sample_screenplay_text():
    fixture_path = os.path.join(os.path.dirname(__file__), "fixtures", "sample_screenplay.txt")
    with open(fixture_path, "r", encoding="utf-8") as f:
        return f.read()


def test_pydantic_scene_analysis_model():
    """Test that SceneAnalysis model validates all 11 required production parameters."""
    dependency = ProductionDependency(
        dependency_type="Stunt Rigging",
        description="Overhead paracord wire harness for falling scene",
        required_by_department="Stunts"
    )
    risk = ProductionRisk(
        risk_category="Safety",
        description="Potential fall hazard near roof parapet",
        severity="HIGH",
        mitigation_notes="Safety harness and spotter mandatory"
    )

    scene = SceneAnalysis(
        scene_number="10A",
        scene_description="Hero leaps across roof edge in rainstorm.",
        location_type=SceneLocationType.EXT,
        location_name="ROOFTOP - NIGHT",
        time_of_day=TimeOfDay.NIGHT,
        characters=["HERO", "VILLAIN"],
        props=["Grappling Hook"],
        weather_environment=["Torrential Rain"],
        special_production_requirements=["High-speed Phantom Camera"],
        production_dependencies=[dependency],
        potential_production_risks=[risk]
    )

    # Verify all 11 fields exist and match input
    assert scene.scene_number == "10A"
    assert scene.scene_description == "Hero leaps across roof edge in rainstorm."
    assert scene.location_type == SceneLocationType.EXT
    assert scene.location_name == "ROOFTOP - NIGHT"
    assert scene.time_of_day == TimeOfDay.NIGHT
    assert "HERO" in scene.characters
    assert "Grappling Hook" in scene.props
    assert "Torrential Rain" in scene.weather_environment
    assert "High-speed Phantom Camera" in scene.special_production_requirements
    assert len(scene.production_dependencies) == 1
    assert scene.production_dependencies[0].dependency_type == "Stunt Rigging"
    assert len(scene.potential_production_risks) == 1
    assert scene.potential_production_risks[0].severity == "HIGH"


def test_pydantic_production_analysis_serialization():
    """Test full breakdown serialization to/from JSON."""
    analysis = ScreenplayProductionAnalysis(
        title="Test Production Script",
        total_scenes=1,
        scenes=[
            SceneAnalysis(
                scene_number="1",
                scene_description="Intro scene",
                location_type=SceneLocationType.INT,
                location_name="LAB - DAY",
                time_of_day=TimeOfDay.DAY,
                characters=["Dr. Smith"],
                props=["Microscope"],
                weather_environment=["Controlled Climate"],
                special_production_requirements=[],
                production_dependencies=[],
                potential_production_risks=[]
            )
        ],
        all_characters=["Dr. Smith"],
        all_props=["Microscope"],
        high_risk_scenes=[],
        summary="Simple test script breakdown."
    )

    json_str = analysis.model_dump_json()
    reconstructed = ScreenplayProductionAnalysis.model_validate_json(json_str)

    assert reconstructed.title == "Test Production Script"
    assert reconstructed.total_scenes == 1
    assert reconstructed.scenes[0].characters == ["Dr. Smith"]


def test_mock_screenplay_parser_service(sample_screenplay_text):
    """
    Test deterministic mock analysis mode.
    Ensures zero live Gemini calls are made and structured output contains all required fields.
    """
    parser = ScreenplayParserService()
    result = parser.analyze_script_text(sample_screenplay_text, mock_mode=True)

    assert isinstance(result, ScreenplayProductionAnalysis)
    assert result.total_scenes > 0
    assert len(result.scenes) == result.total_scenes

    # Check 11 required parameters on scenes
    for scene in result.scenes:
        assert scene.scene_number is not None
        assert scene.scene_description != ""
        assert scene.location_type in [SceneLocationType.INT, SceneLocationType.EXT, SceneLocationType.INT_EXT, SceneLocationType.OTHER]
        assert scene.location_name != ""
        assert scene.time_of_day in [TimeOfDay.DAY, TimeOfDay.NIGHT, TimeOfDay.DUSK, TimeOfDay.DAWN, TimeOfDay.CONTINUOUS, TimeOfDay.SAME, TimeOfDay.UNKNOWN]
        assert isinstance(scene.characters, list)
        assert isinstance(scene.props, list)
        assert isinstance(scene.weather_environment, list)
        assert isinstance(scene.special_production_requirements, list)
        assert isinstance(scene.production_dependencies, list)
        assert isinstance(scene.potential_production_risks, list)


def test_pdf_extractor_service_file_not_found():
    """Test PDF service handles missing file error cleanly."""
    pdf_service = PDFExtractorService()
    with pytest.raises(FileNotFoundError):
        pdf_service.extract_text_from_pdf_path("non_existent_file.pdf")


def test_pdf_extractor_service_empty_bytes():
    """Test PDF service handles empty bytes error cleanly."""
    pdf_service = PDFExtractorService()
    with pytest.raises(ValueError):
        pdf_service.extract_text_from_pdf_bytes(b"")


def test_agent_model_configurable():
    """Test that screenplay_agent receives model configured from environment variable."""
    assert screenplay_agent.name == "screenplay_agent"
    assert screenplay_agent.model is not None
    # Verify default or env-configured model
    expected_model = os.getenv("CINEOPS_GEMINI_MODEL", os.getenv("GEMINI_MODEL", "gemini-2.5-flash"))
    assert screenplay_agent.model == expected_model
