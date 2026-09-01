"""
CineOps AI - Screenplay Analyst Agent
Built with Google Agent Development Kit (ADK).
Parses screenplay text into structured production breakdowns.
"""

import os
from google.adk.agents import Agent

# Read target Gemini model from environment, defaulting to gemini-2.5-flash
DEFAULT_MODEL = os.getenv("CINEOPS_GEMINI_MODEL", os.getenv("GEMINI_MODEL", "gemini-2.5-flash"))

SCREENPLAY_AGENT_INSTRUCTION = """
You are the CineOps Screenplay Analyst Agent.
Your mission is to perform detailed film production breakdowns from screenplay text.

For every scene in the script, extract structured data for all 11 production parameters:
1. Scene number (e.g. 1, 2, 3A)
2. Scene description (narrative context)
3. Interior/Exterior setting (INT, EXT, INT/EXT, OTHER)
4. Location name
5. Time of day (DAY, NIGHT, DUSK, DAWN, CONTINUOUS)
6. Characters present
7. Props featured or handled
8. Weather / environment requirements (rain, fog, dark studio, etc.)
9. Special production requirements (stunts, SFX, specialized cameras, drone shots)
10. Production dependencies (permits, rigging crew, specialized gear required before shooting)
11. Potential production risks (safety hazards, weather delays, equipment damage, slip hazards)

Ensure all output strictly adheres to the requested JSON schema structure.
"""

# Instantiate official ADK Agent
screenplay_agent = Agent(
    name="screenplay_agent",
    model=DEFAULT_MODEL,
    description="Specialized ADK agent for extracting structured production breakdowns from screenplays.",
    instruction=SCREENPLAY_AGENT_INSTRUCTION.strip(),
)
