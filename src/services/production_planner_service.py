"""
CineOps AI - Production Planner Service
Orchestrates production planning by reasoning over structured screenplay analyses
and Parallel web research data. Operates in 100% offline mock mode by default when billing is pending.
"""

import json
import os
from typing import Optional
from google.adk.runners import InMemoryRunner
from google.genai import types

from src.models.planner import (
    ProductionPlan,
    ResearchReference,
    ResourceRequirement,
    SceneGroup,
    ShootingScheduleDay,
)
from src.models.production import ScreenplayProductionAnalysis
from src.models.screenplay import ProductionRisk
from src.services.parallel_search import ProductionResearchResponse, ResearchResultItem


class ProductionPlannerService:
    """
    Service responsible for synthesizing screenplay analysis and research results into structured production plans.
    """

    def __init__(self, agent=None):
        if agent is None:
            from src.agents.production_planner_agent import production_planner_agent
            self.agent = production_planner_agent
        else:
            self.agent = agent

    def generate_plan(
        self,
        analysis: ScreenplayProductionAnalysis,
        research_data: Optional[ProductionResearchResponse] = None,
        mock_mode: Optional[bool] = None,
    ) -> ProductionPlan:
        """
        Synchronous entry point for generating a production plan.
        If mock_mode is True (or env CINEOPS_MOCK_MODE=1), runs 100% offline with zero network calls.
        """
        if mock_mode is None:
            mock_mode = os.getenv("CINEOPS_MOCK_MODE", "1") == "1"

        if mock_mode:
            return self._generate_mock_plan(analysis, research_data)
        else:
            import asyncio
            return asyncio.run(self._generate_with_adk(analysis, research_data))

    async def generate_plan_async(
        self,
        analysis: ScreenplayProductionAnalysis,
        research_data: Optional[ProductionResearchResponse] = None,
        mock_mode: Optional[bool] = None,
    ) -> ProductionPlan:
        """
        Asynchronous entry point for generating a production plan.
        """
        if mock_mode is None:
            mock_mode = os.getenv("CINEOPS_MOCK_MODE", "1") == "1"

        if mock_mode:
            return self._generate_mock_plan(analysis, research_data)
        else:
            return await self._generate_with_adk(analysis, research_data)

    def _generate_mock_plan(
        self,
        analysis: ScreenplayProductionAnalysis,
        research_data: Optional[ProductionResearchResponse] = None,
    ) -> ProductionPlan:
        """
        Deterministic, offline mock plan generator.
        Performs scene grouping, scheduling, resource aggregation, and research integration with zero network calls.
        """
        # 1. Scene Grouping Logic: Group scenes sharing location / environment
        grouped_by_loc = {}
        for scene in analysis.scenes:
            loc = scene.location_name or "UNKNOWN LOCATION"
            if loc not in grouped_by_loc:
                grouped_by_loc[loc] = []
            grouped_by_loc[loc].append(scene.scene_number)

        scene_groups = []
        for idx, (loc_name, scene_nums) in enumerate(grouped_by_loc.items(), start=1):
            scene_groups.append(
                SceneGroup(
                    group_id=f"GRP-{idx:02d}",
                    group_name=f"Location Unit: {loc_name}",
                    scene_numbers=scene_nums,
                    location_name=loc_name,
                    grouping_reason=f"Consolidates scenes shooting at {loc_name} to eliminate redundant location teardown.",
                )
            )

        # 2. Recommended Shooting Schedule: Day-by-day scheduling
        shooting_schedule = []
        day_counter = 1
        for group in scene_groups:
            shooting_schedule.append(
                ShootingScheduleDay(
                    day_number=day_counter,
                    title=f"Principal Photography Day {day_counter}: {group.location_name}",
                    scene_numbers=group.scene_numbers,
                    estimated_hours=10.0 if "NIGHT" in group.location_name or "DAWN" in group.location_name else 8.0,
                    location=group.location_name,
                    notes_and_rationale=f"Execute scenes {', '.join(group.scene_numbers)} sequentially. Priority given to lighting setups.",
                )
            )
            day_counter += 1

        # 3. Location Recommendations
        location_recommendations = [
            f"Scout accessible urban location matching {loc} with adequate power access and holding space."
            for loc in grouped_by_loc.keys()
        ]

        # 4. Resource Requirements Consolidation
        resources = []
        seen_items = set()
        for scene in analysis.scenes:
            for prop in scene.props:
                if prop not in seen_items:
                    seen_items.add(prop)
                    resources.append(
                        ResourceRequirement(
                            category="Props",
                            item_name=prop,
                            required_for_scenes=[scene.scene_number],
                            specification_details=f"Featured prop handled in Scene {scene.scene_number}",
                        )
                    )

            for dep in scene.production_dependencies:
                dep_key = f"{dep.dependency_type}:{dep.description}"
                if dep_key not in seen_items:
                    seen_items.add(dep_key)
                    resources.append(
                        ResourceRequirement(
                            category=dep.dependency_type or "Permit / Logistics",
                            item_name=dep.description,
                            required_for_scenes=[scene.scene_number],
                            specification_details=f"Required by department: {dep.required_by_department or 'Production'}",
                        )
                    )

        # 5. Production Risks Consolidation
        all_risks = []
        for scene in analysis.scenes:
            all_risks.extend(scene.potential_production_risks)

        # Fallback risk if script has none
        if not all_risks:
            all_risks.append(
                ProductionRisk(
                    risk_category="General Safety",
                    description="Standard set activity hazards during night shoots",
                    severity="LOW",
                    mitigation_notes="Ensure safety briefing prior to first call",
                )
            )

        # 6. Research References Integration (Offline mock data if none passed)
        references = []
        if research_data and research_data.results:
            for item in research_data.results:
                references.append(
                    ResearchReference(
                        topic=research_data.objective,
                        title=item.title or "Parallel Research Result",
                        url=item.url,
                        key_insight=item.excerpts[0] if item.excerpts else "Verified safety and technical requirements.",
                    )
                )
        else:
            # Offline mock research references (zero API calls)
            references.append(
                ResearchReference(
                    topic="Wet-down and Rain Machine Safety Guidelines",
                    title="Industry Film Safety Bulletin - Water & Wet Sets",
                    url="https://safety.industryfilm.org/bulletins/wet-sets",
                    key_insight="All electrical equipment operated near water effects must use GFCI breakers and insulated cabling.",
                )
            )
            references.append(
                ResearchReference(
                    topic="Commercial Drone Aerial Filming Regulations",
                    title="FAA Part 107 Commercial Drone Operating Rules",
                    url="https://faa.gov/uas/commercial_operators",
                    key_insight="Operation over people requires certified Category 1-4 UAS or dedicated closed-set perimeter.",
                )
            )

        # 7. Strategic Reasoning
        strategic_reasoning = (
            f"The production plan optimizes the shooting schedule into {len(shooting_schedule)} principal days. "
            f"Scenes are grouped strictly by location ({', '.join(grouped_by_loc.keys())}) to minimize company moves. "
            f"Night and rain scenes are scheduled with safety buffers and GFCI electrical protection as informed by Parallel research."
        )

        return ProductionPlan(
            title=f"Production Plan - {analysis.title}",
            overall_summary=f"Comprehensive production plan covering {analysis.total_scenes} scenes across {len(shooting_schedule)} shooting days with full risk mitigations.",
            total_estimated_days=len(shooting_schedule),
            scene_groupings=scene_groups,
            shooting_schedule=shooting_schedule,
            location_recommendations=location_recommendations,
            resource_requirements=resources,
            production_risks=all_risks,
            research_references=references,
            strategic_reasoning=strategic_reasoning,
        )

    async def _generate_with_adk(
        self,
        analysis: ScreenplayProductionAnalysis,
        research_data: Optional[ProductionResearchResponse] = None,
    ) -> ProductionPlan:
        """
        Live ADK execution via Gemini API.
        Called when mock_mode=False and billing is active.
        """
        runner = InMemoryRunner(agent=self.agent, app_name="cineops_planner_app")
        user_id = "planner_user"
        session_id = "planner_session"

        await runner.session_service.create_session(
            user_id=user_id,
            session_id=session_id,
            app_name=runner.app_name
        )

        research_context = ""
        if research_data:
            research_context = f"\nRelevant Research Data:\n{research_data.model_dump_json(indent=2)}"

        prompt = (
            f"Synthesize the following screenplay analysis into a structured ProductionPlan JSON object.\n\n"
            f"Screenplay Analysis:\n{analysis.model_dump_json(indent=2)}\n"
            f"{research_context}"
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

        # Extract clean JSON block from markdown if present
        cleaned_json = full_response_text.strip()
        if cleaned_json.startswith("```json"):
            cleaned_json = cleaned_json[7:]
        if cleaned_json.startswith("```"):
            cleaned_json = cleaned_json[3:]
        if cleaned_json.endswith("```"):
            cleaned_json = cleaned_json[:-3]
        cleaned_json = cleaned_json.strip()

        return ProductionPlan.model_validate_json(cleaned_json)
