"""
CineOps AI - Production Planner Unit Tests
Tests for Pydantic production plan models, scene grouping, shooting schedule,
risk evaluation, research integration, and zero-network mock execution mode.
"""

import os
from unittest.mock import patch
import pytest

from src.models.planner import (
    ProductionPlan,
    ResearchReference,
    ResourceRequirement,
    SceneGroup,
    ShootingScheduleDay,
)
from src.models.production import ScreenplayProductionAnalysis
from src.models.screenplay import (
    ProductionDependency,
    ProductionRisk,
    SceneAnalysis,
    SceneLocationType,
    TimeOfDay,
)
from src.services.parallel_search import ProductionResearchResponse, ResearchResultItem
from src.services.production_planner_service import ProductionPlannerService
from src.services.screenplay_parser import ScreenplayParserService


@pytest.fixture
def sample_analysis():
    """Provides a sample ScreenplayProductionAnalysis object with multiple scenes."""
    scene_1 = SceneAnalysis(
        scene_number="1",
        scene_description="Alleyway confrontation in rain.",
        location_type=SceneLocationType.EXT,
        location_name="ABANDONED ALLEYWAY - NIGHT",
        time_of_day=TimeOfDay.NIGHT,
        characters=["MILLER", "DAVIS"],
        props=["Flashlight", "Vintage Revolver"],
        weather_environment=["Heavy Rain"],
        special_production_requirements=["Rain machine"],
        production_dependencies=[
            ProductionDependency(dependency_type="Permit", description="Alleyway night permit")
        ],
        potential_production_risks=[
            ProductionRisk(risk_category="Safety", description="Slippery surface", severity="MEDIUM")
        ],
    )

    scene_2 = SceneAnalysis(
        scene_number="2",
        scene_description="Precinct evidence review.",
        location_type=SceneLocationType.INT,
        location_name="POLICE PRECINCT - OFFICE - NIGHT",
        time_of_day=TimeOfDay.NIGHT,
        characters=["MILLER", "HENDERSON"],
        props=["Tablet Computer"],
        weather_environment=["Controlled Dim Lighting"],
        special_production_requirements=[],
        production_dependencies=[],
        potential_production_risks=[],
    )

    scene_3 = SceneAnalysis(
        scene_number="3",
        scene_description="Alleyway follow-up investigation.",
        location_type=SceneLocationType.EXT,
        location_name="ABANDONED ALLEYWAY - NIGHT",
        time_of_day=TimeOfDay.NIGHT,
        characters=["MILLER"],
        props=["Evidence Bag"],
        weather_environment=["Wet Pavement"],
        special_production_requirements=[],
        production_dependencies=[],
        potential_production_risks=[],
    )

    return ScreenplayProductionAnalysis(
        title="Test Screenplay Analysis",
        total_scenes=3,
        scenes=[scene_1, scene_2, scene_3],
        all_characters=["MILLER", "DAVIS", "HENDERSON"],
        all_props=["Flashlight", "Vintage Revolver", "Tablet Computer", "Evidence Bag"],
        high_risk_scenes=[],
        summary="Test screenplay analysis for unit tests.",
    )


def test_production_plan_pydantic_validation():
    """Test ProductionPlan model serialization and deserialization."""
    plan = ProductionPlan(
        title="Test Production Roadmap",
        overall_summary="Executive summary for test production plan.",
        total_estimated_days=2,
        scene_groupings=[
            SceneGroup(
                group_id="GRP-01",
                group_name="Alleyway Scenes",
                scene_numbers=["1", "3"],
                location_name="ABANDONED ALLEYWAY - NIGHT",
                grouping_reason="Shared exterior location",
            )
        ],
        shooting_schedule=[
            ShootingScheduleDay(
                day_number=1,
                title="Alleyway Unit Shoot",
                scene_numbers=["1", "3"],
                estimated_hours=10.0,
                location="ABANDONED ALLEYWAY - NIGHT",
                notes_and_rationale="Shoot rain sequences continuously.",
            )
        ],
        location_recommendations=["Scout cobblestone alleyway in industrial zone."],
        resource_requirements=[
            ResourceRequirement(
                category="Props",
                item_name="Vintage Revolver",
                required_for_scenes=["1"],
            )
        ],
        production_risks=[
            ProductionRisk(
                risk_category="Safety",
                description="Slippery cobblestones",
                severity="MEDIUM",
                mitigation_notes="Use anti-slip mats",
            )
        ],
        research_references=[
            ResearchReference(
                topic="Rain machine safety",
                title="Film Safety Guide",
                url="https://safety.example.com",
                key_insight="Use GFCI protection",
            )
        ],
        strategic_reasoning="Consolidated locations to minimize teardown.",
    )

    json_str = plan.model_dump_json()
    reconstructed = ProductionPlan.model_validate_json(json_str)

    assert reconstructed.title == "Test Production Roadmap"
    assert len(reconstructed.scene_groupings) == 1
    assert reconstructed.scene_groupings[0].scene_numbers == ["1", "3"]
    assert reconstructed.total_estimated_days == 2


def test_mock_planner_service_generation(sample_analysis):
    """Test deterministic mock plan generation with zero network calls."""
    planner = ProductionPlannerService()
    plan = planner.generate_plan(sample_analysis, mock_mode=True)

    assert isinstance(plan, ProductionPlan)
    assert plan.total_estimated_days > 0
    assert len(plan.scene_groupings) > 0
    assert len(plan.shooting_schedule) == plan.total_estimated_days
    assert len(plan.resource_requirements) > 0
    assert len(plan.production_risks) > 0
    assert len(plan.research_references) > 0


def test_scene_grouping_logic(sample_analysis):
    """Test that scenes sharing the same location are correctly grouped together."""
    planner = ProductionPlannerService()
    plan = planner.generate_plan(sample_analysis, mock_mode=True)

    # In sample_analysis, Scene 1 and Scene 3 share 'ABANDONED ALLEYWAY - NIGHT'
    alleyway_group = None
    for group in plan.scene_groupings:
        if group.location_name == "ABANDONED ALLEYWAY - NIGHT":
            alleyway_group = group
            break

    assert alleyway_group is not None
    assert "1" in alleyway_group.scene_numbers
    assert "3" in alleyway_group.scene_numbers


def test_research_integration(sample_analysis):
    """Test that provided Parallel research results are incorporated into research references."""
    custom_research = ProductionResearchResponse(
        objective="High-speed drone permits",
        search_queries=["FAA drone permit"],
        results=[
            ResearchResultItem(
                title="FAA Drone Regulations",
                url="https://faa.gov/drone-rules",
                excerpts=["Part 107 waiver required for night flight over people"],
            )
        ],
        search_id="drone_test_001",
        total_results=1,
    )

    planner = ProductionPlannerService()
    plan = planner.generate_plan(sample_analysis, research_data=custom_research, mock_mode=True)

    # Verify custom research item exists in research_references
    faa_ref = None
    for ref in plan.research_references:
        if "faa.gov" in ref.url:
            faa_ref = ref
            break

    assert faa_ref is not None
    assert faa_ref.title == "FAA Drone Regulations"
    assert "Part 107" in faa_ref.key_insight


@patch("requests.post")
@patch("google.genai.Client")
def test_zero_network_calls_in_mock_mode(mock_genai, mock_post, sample_analysis):
    """Verify that no external API calls (requests or genai) occur during mock mode execution."""
    parser = ScreenplayParserService()
    planner = ProductionPlannerService()

    # Run full mock pipeline
    script_analysis = parser._generate_mock_analysis("dummy text")
    plan = planner.generate_plan(script_analysis, mock_mode=True)

    # Ensure zero network calls were attempted
    mock_post.assert_not_called()
    mock_genai.assert_not_called()
    assert plan is not None
