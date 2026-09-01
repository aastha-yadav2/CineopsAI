"""
CineOps AI - Main End-to-End Pipeline Runner
Executes full autonomous film production pipeline:
Screenplay Text -> Screenplay Analyst Agent -> Parallel Research Service -> Production Planner Agent -> Production Plan

Default mode is 100% offline mock mode to prevent paid API calls while billing is pending.
"""

import json
import os
import sys
from pathlib import Path

# Add project root directory to sys.path
ROOT_DIR = Path(__file__).resolve().parent.parent
if str(ROOT_DIR) not in sys.path:
    sys.path.insert(0, str(ROOT_DIR))

from dotenv import load_dotenv
from src.agents import cineops_agent, screenplay_agent, production_planner_agent
from src.services import (
    ScreenplayParserService,
    ParallelSearchService,
    ProductionPlannerService,
)


def run_cineops_pipeline(mock_mode: bool = True):
    load_dotenv()

    model_name = os.getenv("CINEOPS_GEMINI_MODEL", os.getenv("GEMINI_MODEL", "gemini-2.5-flash"))

    print("=" * 75)
    print("      CineOps AI - Autonomous Film Production Planning Pipeline      ")
    print("=" * 75)
    print(f"Root Agent       : {cineops_agent.name}")
    print(f"Screenplay Agent : {screenplay_agent.name}")
    print(f"Planner Agent    : {production_planner_agent.name}")
    print(f"Configured Model : {model_name}")
    print(f"Execution Mode   : {'OFFLINE MOCK MODE (Billing Pending)' if mock_mode else 'LIVE ADK & PARALLEL MODE'}")
    print("=" * 75)

    # 1. Load sample screenplay text
    fixture_path = os.path.join(os.path.dirname(__file__), "..", "tests", "fixtures", "sample_screenplay.txt")
    if not os.path.exists(fixture_path):
        print(f"ERROR: Sample screenplay fixture not found at {fixture_path}", file=sys.stderr)
        return False

    with open(fixture_path, "r", encoding="utf-8") as f:
        script_text = f.read()

    print(f"\n[STAGE 1: SCREENPLAY ANALYSIS]")
    print(f"Ingesting Screenplay ({len(script_text)} characters)...")
    parser = ScreenplayParserService()
    analysis_result = parser.analyze_script_text(script_text, mock_mode=mock_mode)
    print(f"[OK] Parsed {analysis_result.total_scenes} scenes successfully.")
    print(f"  Characters Identified : {len(analysis_result.all_characters)} ({', '.join(analysis_result.all_characters[:3])}...)")
    print(f"  Props Identified      : {len(analysis_result.all_props)}")

    # 2. Parallel Research Stage
    print(f"\n[STAGE 2: PARALLEL PRODUCTION RESEARCH]")
    objective = "Find film set safety regulations for outdoor night wet-down rain scenes and rooftop drone permits."
    queries = [
        "film set rain machine safety guidelines",
        "outdoor night shoot wet down electrical safety",
        "FAA drone permit commercial rooftop filming"
    ]
    print(f"Research Objective : {objective}")

    research_data = None
    if not mock_mode:
        parallel_key = os.getenv("PARALLEL_API_KEY")
        if parallel_key:
            print("Querying live Parallel Search API (api.parallel.ai)...")
            search_service = ParallelSearchService(api_key=parallel_key)
            research_data = search_service.search(objective=objective, search_queries=queries)
            print(f"[OK] Retrieved {research_data.total_results} live research references.")
        else:
            print("WARNING: PARALLEL_API_KEY missing in live mode; proceeding with mock research.")
    else:
        print("[OK] Offline mock mode active: Using pre-structured Parallel research data (0 API calls).")

    # 3. Production Planning Stage
    print(f"\n[STAGE 3: PRODUCTION PLANNER AGENT REASONING]")
    print("Synthesizing scene groupings, day-by-day schedule, resources, and risk mitigations...")
    planner = ProductionPlannerService()
    production_plan = planner.generate_plan(
        analysis=analysis_result,
        research_data=research_data,
        mock_mode=mock_mode
    )
    print(f"[OK] Generated {production_plan.total_estimated_days}-day production plan.")

    # 4. Display Final Output
    print("\n" + "=" * 75)
    print("               FINAL PRODUCTION PLAN (Pydantic Validated)              ")
    print("=" * 75)
    print(json.dumps(production_plan.model_dump(), indent=2))
    print("=" * 75)

    print("\n[PIPELINE EXECUTION SUMMARY]")
    print(f"- Total Shooting Days       : {production_plan.total_estimated_days}")
    print(f"- Location Scene Groups     : {len(production_plan.scene_groupings)}")
    print(f"- Resource Requirements     : {len(production_plan.resource_requirements)}")
    print(f"- Identified Production Risks: {len(production_plan.production_risks)}")
    print(f"- Research References Cited : {len(production_plan.research_references)}")
    print("\nSUCCESS: CineOps AI end-to-end pipeline completed cleanly!")
    return True


def main():
    try:
        live_flag = "--live" in sys.argv
        mock_env = os.getenv("CINEOPS_MOCK_MODE", "1") == "1"
        mock_mode = not live_flag and mock_env

        success = run_cineops_pipeline(mock_mode=mock_mode)
        if not success:
            sys.exit(1)
    except Exception as e:
        print(f"\nERROR: Failed executing CineOps pipeline: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
