"""
CineOps AI - Screenplay Parser Service
Analyzes screenplay text and produces structured production breakdown objects.
Supports simple deterministic mock mode for offline testing without Gemini billing.
"""

import json
import os
from typing import Optional
from google.adk.runners import InMemoryRunner
from google.genai import types

from src.agents.screenplay_agent import screenplay_agent
from src.models.production import ScreenplayProductionAnalysis
from src.models.screenplay import (
    SceneAnalysis,
    SceneLocationType,
    TimeOfDay,
    ProductionDependency,
    ProductionRisk,
)


class ScreenplayParserService:
    """
    Service for parsing screenplay text into structured production analyses.
    """

    def __init__(self, agent=None):
        self.agent = agent or screenplay_agent

    def analyze_script_text(
        self, script_text: str, mock_mode: Optional[bool] = None
    ) -> ScreenplayProductionAnalysis:
        """
        Synchronous entry point for screenplay analysis.
        If mock_mode is True (or env CINEOPS_MOCK_MODE=1), returns deterministic test analysis.
        """
        if mock_mode is None:
            mock_mode = os.getenv("CINEOPS_MOCK_MODE", "1") == "1"

        if mock_mode:
            return self._generate_mock_analysis(script_text)
        else:
            import asyncio
            return asyncio.run(self._analyze_with_adk(script_text))

    async def analyze_script_text_async(
        self, script_text: str, mock_mode: Optional[bool] = None
    ) -> ScreenplayProductionAnalysis:
        """
        Asynchronous entry point for screenplay analysis.
        """
        if mock_mode is None:
            mock_mode = os.getenv("CINEOPS_MOCK_MODE", "1") == "1"

        if mock_mode:
            return self._generate_mock_analysis(script_text)
        else:
            return await self._analyze_with_adk(script_text)

    def _generate_mock_analysis(self, script_text: str) -> ScreenplayProductionAnalysis:
        """
        Intentionally simple deterministic mock breakdown for local testing while billing is pending.
        Exposes all 11 required production parameters.
        """
        # Create deterministic mock scene breakdowns
        scene_1 = SceneAnalysis(
            scene_number="1",
            scene_description="Detective Miller inspects a rain-soaked abandoned alleyway under dim streetlights.",
            location_type=SceneLocationType.EXT,
            location_name="ABANDONED ALLEYWAY - NIGHT",
            time_of_day=TimeOfDay.NIGHT,
            characters=["DETECTIVE MILLER", "OFFICER DAVIS"],
            props=["Vintage Revolver", "Leather Trench Coat", "Flashlight", "Evidence Bag"],
            weather_environment=["Heavy Rain", "Wet Pavement", "Low Fog"],
            special_production_requirements=[
                "Wet-down crew required for alley surface",
                "Rain machine setup",
                "Atmospheric fogger"
            ],
            production_dependencies=[
                ProductionDependency(
                    dependency_type="Permit",
                    description="City alleyway night shooting permit and noise waiver after 10 PM",
                    required_by_department="Logistics"
                ),
                ProductionDependency(
                    dependency_type="Equipment",
                    description="Waterproof camera housing and rain covers",
                    required_by_department="Camera"
                )
            ],
            potential_production_risks=[
                ProductionRisk(
                    risk_category="Safety",
                    description="Slippery cobblestones under heavy rain setup",
                    severity="MEDIUM",
                    mitigation_notes="Apply anti-slip grips and post safety monitors near wet zones"
                )
            ]
        )

        scene_2 = SceneAnalysis(
            scene_number="2",
            scene_description="Miller enters the dimly lit precinct office to analyze retrieved evidence on a tablet.",
            location_type=SceneLocationType.INT,
            location_name="POLICE PRECINCT - OFFICE - NIGHT",
            time_of_day=TimeOfDay.NIGHT,
            characters=["DETECTIVE MILLER", "CAPTAIN HENDERSON"],
            props=["Tablet Computer", "Coffee Cup", "Case File Folder"],
            weather_environment=["Interior Studio", "Controlled Dim Lighting"],
            special_production_requirements=[
                "Practical monitor playback graphics for evidence display",
                "Practical desk lamps with blue gel color grade"
            ],
            production_dependencies=[
                ProductionDependency(
                    dependency_type="Art",
                    description="Prop tablet with animated evidence UI loaded",
                    required_by_department="Props"
                )
            ],
            potential_production_risks=[
                ProductionRisk(
                    risk_category="Technical",
                    description="Screen glare on tablet screen during close-up camera moves",
                    severity="LOW",
                    mitigation_notes="Use anti-glare screen filter and matte lighting polarizers"
                )
            ]
        )

        scene_3 = SceneAnalysis(
            scene_number="3",
            scene_description="Industrial warehouse rooftop confrontation at dawn with pyrotechnic stunt squib.",
            location_type=SceneLocationType.EXT,
            location_name="WAREHOUSE ROOFTOP - DAWN",
            time_of_day=TimeOfDay.DAWN,
            characters=["DETECTIVE MILLER", "SUSPECT X", "STUNT DOUBLE"],
            props=["Sniper Rifle", "Paracord Rig", "Smoke Grenade"],
            weather_environment=["Dawn Sunlight", "High Wind Hazards"],
            special_production_requirements=[
                "Stunt harness and fall safety airbags",
                "Drone aerial filming permit",
                "Practical pyrotechnic spark squibs"
            ],
            production_dependencies=[
                ProductionDependency(
                    dependency_type="Crew",
                    description="Certified Stunt Coordinator & Pyrotechnics Safety Officer on set",
                    required_by_department="Stunts / SFX"
                ),
                ProductionDependency(
                    dependency_type="Permit",
                    description="FAA Drone flight zone authorization for industrial rooftop",
                    required_by_department="Logistics"
                )
            ],
            potential_production_risks=[
                ProductionRisk(
                    risk_category="Safety",
                    description="High altitude rooftop edge action sequence with pyrotechnics",
                    severity="HIGH",
                    mitigation_notes="Stunt harness required for all talent near roof boundary; dedicated SFX medic on stand-by"
                )
            ]
        )

        return ScreenplayProductionAnalysis(
            title="CineOps Sample Screenplay Analysis (Mock Mode)",
            total_scenes=3,
            scenes=[scene_1, scene_2, scene_3],
            all_characters=["DETECTIVE MILLER", "OFFICER DAVIS", "CAPTAIN HENDERSON", "SUSPECT X", "STUNT DOUBLE"],
            all_props=["Vintage Revolver", "Leather Trench Coat", "Flashlight", "Evidence Bag", "Tablet Computer", "Coffee Cup", "Case File Folder", "Sniper Rifle", "Paracord Rig", "Smoke Grenade"],
            high_risk_scenes=["3"],
            summary="Analysis completed in deterministic mock mode. Script contains 3 scenes with high-risk stunt/pyrotechnic sequences in Scene 3 requiring specialized safety officers, drone permits, and wet-down rain setups."
        )

    async def _analyze_with_adk(self, script_text: str) -> ScreenplayProductionAnalysis:
        """
        Live ADK execution via Gemini API.
        Called when mock_mode=False and billing is active.
        """
        runner = InMemoryRunner(agent=self.agent, app_name="cineops_analysis_app")
        user_id = "analyst_user"
        session_id = "analysis_session"

        await runner.session_service.create_session(
            user_id=user_id,
            session_id=session_id,
            app_name=runner.app_name
        )

        prompt = (
            f"Analyze the following screenplay text and return a valid JSON object matching the ScreenplayProductionAnalysis schema.\n\n"
            f"Screenplay Text:\n{script_text}"
        )

        user_message = types.Content(
            role="user",
            parts=[types.Part.from_text(text=prompt)]
        )

        full_response_text = ""
        async for event in runner.run_async(
            user_id=user_id,
            session_id=session_id,
            new_message=user_message
        ):
            if event.content and event.content.parts:
                for part in event.content.parts:
                    if part.text:
                        full_response_text += part.text

        # Extract JSON block if response contains markdown formatting
        cleaned_json = full_response_text.strip()
        if cleaned_json.startswith("```json"):
            cleaned_json = cleaned_json[7:]
        if cleaned_json.startswith("```"):
            cleaned_json = cleaned_json[3:]
        if cleaned_json.endswith("```"):
            cleaned_json = cleaned_json[:-3]
        cleaned_json = cleaned_json.strip()

        return ScreenplayProductionAnalysis.model_validate_json(cleaned_json)
