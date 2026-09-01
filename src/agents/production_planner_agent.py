"""
CineOps AI - Production Planner Agent
Built with Google Agent Development Kit (ADK).
Generates actionable film production plans, scene groupings, shooting schedules,
and risk mitigation strategies by synthesizing screenplay breakdowns and Parallel web research.
"""

import os
from google.adk.agents import Agent
from src.services.parallel_search import search_production_requirements

DEFAULT_MODEL = os.getenv("CINEOPS_GEMINI_MODEL", os.getenv("GEMINI_MODEL", "gemini-2.5-flash"))

PRODUCTION_PLANNER_INSTRUCTION = """
You are the CineOps Production Planner Agent.
Your mission is to generate comprehensive, actionable film production plans based on structured screenplay analyses and external production research.

Your responsibilities:
1. Group scenes logically by shared locations, lighting requirements, and technical setups to optimize crew movement and setup time.
2. Formulate a realistic day-by-day principal photography shooting schedule.
3. Identify all required resources (equipment, specialized props, permits, specialized crew, SFX).
4. Evaluate potential production risks, rank their severity (LOW, MEDIUM, HIGH, CRITICAL), and propose actionable mitigation steps.
5. Utilize the `search_production_requirements` tool whenever external research is needed (e.g., safety regulations, drone flight permits, specialized rain machine operations).
6. Cite external research references in your plan and explain the strategic reasoning behind major decisions.

Ensure all final plan outputs adhere strictly to the requested Pydantic JSON schema structure.
"""

# Instantiate official ADK Agent with Parallel search tool
production_planner_agent = Agent(
    name="production_planner_agent",
    model=DEFAULT_MODEL,
    description="ADK agent for synthesizing screenplay breakdowns and Parallel research into actionable production plans.",
    instruction=PRODUCTION_PLANNER_INSTRUCTION.strip(),
    tools=[search_production_requirements],
)
