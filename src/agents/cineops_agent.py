"""
CineOps AI - Core Agent Definition
Autonomous film-production assistant built with Google Agent Development Kit (ADK).
"""

import os
from google.adk.agents import Agent
from src.agents.screenplay_agent import screenplay_agent

DEFAULT_MODEL = os.getenv("CINEOPS_GEMINI_MODEL", os.getenv("GEMINI_MODEL", "gemini-2.5-flash"))

# Define the root agent for CineOps AI
cineops_agent = Agent(
    name="cineops_agent",
    model=DEFAULT_MODEL,
    description="Autonomous film-production assistant for screenplay analysis and production planning.",
    instruction=(
        "You are CineOps AI, an autonomous film-production assistant. "
        "Your primary mission is to analyze screenplays, extract production requirements, "
        "and assist film crews with detailed actionable production plans."
    )
)

# Export root_agent alias as required by ADK conventions
root_agent = cineops_agent
