"""
CineOps AI - Parallel Search Service
Official integration with Parallel Search API (api.parallel.ai / parallel-web).
Used by CineOps AI to conduct external research on production requirements,
equipment specifications, safety guidelines, permits, and risk mitigations.
"""

import json
import os
import sys
from pathlib import Path
from typing import List, Optional
from pydantic import BaseModel, Field
from dotenv import load_dotenv

# Ensure root directory is on sys.path
ROOT_DIR = Path(__file__).resolve().parent.parent.parent
if str(ROOT_DIR) not in sys.path:
    sys.path.insert(0, str(ROOT_DIR))


class ResearchResultItem(BaseModel):
    """Structured representation of a single search result item from Parallel Search API."""
    title: Optional[str] = Field(default="Untitled", description="Title of the webpage or resource")
    url: str = Field(..., description="URL link to the source")
    excerpts: List[str] = Field(default_factory=list, description="Relevant text excerpts extracted by Parallel")
    publish_date: Optional[str] = Field(default=None, description="Publish date if available")


class ProductionResearchResponse(BaseModel):
    """Structured response containing aggregated research results from Parallel Search API."""
    objective: str = Field(..., description="The natural-language research objective provided to Parallel")
    search_queries: List[str] = Field(default_factory=list, description="Search queries executed")
    results: List[ResearchResultItem] = Field(default_factory=list, description="Ranked list of relevant search results")
    search_id: Optional[str] = Field(default=None, description="Unique search query identifier returned by Parallel")
    total_results: int = Field(default=0, description="Total count of results found")


class ParallelSearchService:
    """
    Service for querying official Parallel Search API to gather film production intelligence.
    Reads PARALLEL_API_KEY from environment and never logs API keys.
    """

    def __init__(self, api_key: Optional[str] = None):
        load_dotenv()
        if api_key is not None:
            self._api_key = api_key
        else:
            self._api_key = os.getenv("PARALLEL_API_KEY")

    def __repr__(self) -> str:
        status = "Configured" if self._api_key else "Missing"
        return f"<ParallelSearchService api_key={status}>"

    def search(
        self,
        objective: str,
        search_queries: Optional[List[str]] = None,
        mode: str = "fast"
    ) -> ProductionResearchResponse:
        """
        Execute a search request via Parallel Search API.
        
        Args:
            objective: Natural language statement describing the research goal.
            search_queries: Optional list of explicit keyword search terms.
            mode: Search speed/depth mode ('fast', 'turbo', 'basic', 'advanced').

        Returns:
            ProductionResearchResponse: Validated Pydantic model with search results.
        """
        if not self._api_key or not self._api_key.strip():
            raise ValueError(
                "PARALLEL_API_KEY environment variable is missing or empty. "
                "Please configure PARALLEL_API_KEY in your .env file."
            )

        queries = search_queries if search_queries else [objective]

        # 1. Attempt using official parallel-web SDK
        try:
            from parallel import Parallel
            client = Parallel(api_key=self._api_key)
            raw_response = client.search(
                objective=objective,
                search_queries=queries,
                mode=mode,
                timeout=15.0
            )
            return self._parse_sdk_response(raw_response, objective, queries)
        except ImportError:
            # Fallback to direct REST call if SDK is absent
            return self._search_rest(objective, queries, mode)
        except Exception as err:
            # Mask API key if present in error message
            err_msg = str(err)
            if self._api_key in err_msg:
                err_msg = err_msg.replace(self._api_key, "[REDACTED_API_KEY]")
            raise RuntimeError(f"Parallel Search API call failed: {err_msg}") from None

    def _parse_sdk_response(
        self, raw_response, objective: str, queries: List[str]
    ) -> ProductionResearchResponse:
        """Convert parallel-web SDK SearchResult object into Pydantic model."""
        items = []
        raw_results = getattr(raw_response, "results", []) or []
        for res in raw_results:
            url = getattr(res, "url", "")
            title = getattr(res, "title", None) or "Untitled"
            excerpts = getattr(res, "excerpts", []) or []
            publish_date = getattr(res, "publish_date", None)
            if url:
                items.append(
                    ResearchResultItem(
                        title=title,
                        url=url,
                        excerpts=excerpts,
                        publish_date=publish_date
                    )
                )

        search_id = getattr(raw_response, "search_id", None)
        return ProductionResearchResponse(
            objective=objective,
            search_queries=queries,
            results=items,
            search_id=search_id,
            total_results=len(items)
        )

    def _search_rest(
        self, objective: str, queries: List[str], mode: str
    ) -> ProductionResearchResponse:
        """Direct REST HTTP call to Parallel Search API endpoint (https://api.parallel.ai/v1/search)."""
        import requests

        url = "https://api.parallel.ai/v1/search"
        headers = {
            "Content-Type": "application/json",
            "x-api-key": self._api_key
        }
        payload = {
            "objective": objective,
            "search_queries": queries,
            "mode": mode
        }

        try:
            response = requests.post(url, headers=headers, json=payload, timeout=15.0)
            response.raise_for_status()
            data = response.json()

            items = []
            for item in data.get("results", []):
                items.append(
                    ResearchResultItem(
                        title=item.get("title", "Untitled"),
                        url=item.get("url", ""),
                        excerpts=item.get("excerpts", []),
                        publish_date=item.get("publish_date")
                    )
                )

            return ProductionResearchResponse(
                objective=objective,
                search_queries=queries,
                results=items,
                search_id=data.get("search_id"),
                total_results=len(items)
            )
        except Exception as err:
            err_msg = str(err)
            if self._api_key in err_msg:
                err_msg = err_msg.replace(self._api_key, "[REDACTED_API_KEY]")
            raise RuntimeError(f"Parallel REST API error: {err_msg}") from None


def search_production_requirements(
    objective: str, search_queries: Optional[List[str]] = None
) -> str:
    """
    ADK-compatible tool function for querying Parallel Search API.
    Can be registered with Google ADK agents for autonomous web research.
    """
    service = ParallelSearchService()
    response = service.search(objective=objective, search_queries=search_queries)
    return response.model_dump_json(indent=2)


def run_live_demo():
    """CLI runner to execute a single real Parallel Search API call in explicit live mode."""
    load_dotenv()
    api_key = os.getenv("PARALLEL_API_KEY")

    print("=" * 70)
    print("CineOps AI - Parallel Search Service Live Test")
    print("=" * 70)

    if not api_key or not api_key.strip():
        print("ERROR: PARALLEL_API_KEY is not configured in .env file.", file=sys.stderr)
        print("Please add your key to .env: PARALLEL_API_KEY=your_actual_key", file=sys.stderr)
        sys.exit(1)

    print("Executing 1 real call to Parallel Search API (api.parallel.ai)...")
    service = ParallelSearchService(api_key=api_key)

    objective = "Find film set safety regulations for outdoor night wet-down rain scenes and rain machine operation."
    queries = [
        "film set rain machine safety guidelines",
        "outdoor night shoot wet down electrical safety protocols"
    ]

    print(f"Objective: {objective}")
    print(f"Queries  : {queries}\n")

    res = service.search(objective=objective, search_queries=queries)
    print("=" * 70)
    print("PARALLEL SEARCH API RESPONSE")
    print("=" * 70)
    print(json.dumps(res.model_dump(), indent=2))
    print("=" * 70)
    print(f"\nSUCCESS: Parallel Search returned {res.total_results} structured results.")


if __name__ == "__main__":
    if "--live" in sys.argv:
        run_live_demo()
    else:
        print("CineOps AI - Parallel Search Service Module")
        print("To run an explicit live test against Parallel Search API, execute:")
        print("  .venv\\Scripts\\python.exe src/services/parallel_search.py --live")
