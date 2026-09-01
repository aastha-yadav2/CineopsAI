"""
CineOps AI - Parallel Search Unit Tests
Tests for ParallelSearchService, API key handling, error handling,
and mocked API response processing (zero external HTTP requests required).
"""

import json
import os
from unittest.mock import MagicMock, patch
import pytest

from src.services.parallel_search import (
    ParallelSearchService,
    ProductionResearchResponse,
    ResearchResultItem,
    search_production_requirements,
)


def test_missing_api_key_raises_value_error():
    """Test that missing PARALLEL_API_KEY raises a clear ValueError."""
    service = ParallelSearchService(api_key="")
    with pytest.raises(ValueError) as exc_info:
        service.search(objective="Research rain machine safety")
    assert "PARALLEL_API_KEY environment variable is missing" in str(exc_info.value)


def test_api_key_repr_masking():
    """Test that __repr__ never leaks secret API keys."""
    secret_key = "secret_parallel_key_99999"
    service = ParallelSearchService(api_key=secret_key)
    repr_str = repr(service)
    assert secret_key not in repr_str
    assert "Configured" in repr_str


@patch("parallel.Parallel")
def test_parallel_search_sdk_mocked_success(mock_parallel_cls):
    """Test successful search using mocked parallel-web SDK client."""
    mock_client = MagicMock()
    mock_parallel_cls.return_value = mock_client

    # Create mock result item matching parallel.types.SearchResult
    mock_item = MagicMock()
    mock_item.title = "Film Set Rain Safety Guidelines"
    mock_item.url = "https://safety.industryfilm.org/rain-machines"
    mock_item.excerpts = [
        "All electrical equipment near water rain effects must be powered through GFCI breakers."
    ]
    mock_item.publish_date = "2025-06-15"

    mock_response = MagicMock()
    mock_response.results = [mock_item]
    mock_response.search_id = "search_test_id_101"

    mock_client.search.return_value = mock_response

    service = ParallelSearchService(api_key="test_mock_key")
    result = service.search(
        objective="Research rain machine safety",
        search_queries=["rain machine safety film set"]
    )

    assert isinstance(result, ProductionResearchResponse)
    assert result.objective == "Research rain machine safety"
    assert result.total_results == 1
    assert result.search_id == "search_test_id_101"
    assert result.results[0].title == "Film Set Rain Safety Guidelines"
    assert result.results[0].url == "https://safety.industryfilm.org/rain-machines"
    assert len(result.results[0].excerpts) == 1


@patch("requests.post")
def test_parallel_search_rest_mocked_fallback(mock_post):
    """Test REST fallback method when parallel-web SDK raises or fallback is used."""
    mock_response = MagicMock()
    mock_response.status_code = 200
    mock_response.json.return_value = {
        "search_id": "rest_search_456",
        "results": [
            {
                "title": "OSHA Film Location Guidelines",
                "url": "https://osha.gov/film-guidelines",
                "excerpts": ["Mandatory harness for heights above 6 feet"],
                "publish_date": "2024-01-10"
            }
        ]
    }
    mock_post.return_value = mock_response

    service = ParallelSearchService(api_key="test_mock_key")
    result = service._search_rest(
        objective="Rooftop safety regulations",
        queries=["rooftop film set safety"],
        mode="fast"
    )

    assert isinstance(result, ProductionResearchResponse)
    assert result.total_results == 1
    assert result.results[0].url == "https://osha.gov/film-guidelines"
    assert result.results[0].title == "OSHA Film Location Guidelines"


@patch("src.services.parallel_search.ParallelSearchService.search")
def test_search_production_requirements_tool_function(mock_search):
    """Test ADK-compatible tool wrapper returns valid JSON formatted response."""
    mock_search.return_value = ProductionResearchResponse(
        objective="Drone permit requirements",
        search_queries=["FAA drone permit commercial filming"],
        results=[
            ResearchResultItem(
                title="FAA Part 107 Overview",
                url="https://faa.gov/uas/part107",
                excerpts=["Part 107 license required for commercial drone shoots"]
            )
        ],
        search_id="drone_search_789",
        total_results=1
    )

    json_str_output = search_production_requirements(
        objective="Drone permit requirements",
        search_queries=["FAA drone permit commercial filming"]
    )

    parsed = json.loads(json_str_output)
    assert parsed["objective"] == "Drone permit requirements"
    assert parsed["total_results"] == 1
    assert parsed["results"][0]["url"] == "https://faa.gov/uas/part107"
