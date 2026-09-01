"""
CineOps AI - Screenplay Models
Structured Pydantic schemas for screenplay scene breakdown and production analysis.
"""

from enum import Enum
from typing import List, Optional
from pydantic import BaseModel, Field


class SceneLocationType(str, Enum):
    INT = "INT"
    EXT = "EXT"
    INT_EXT = "INT/EXT"
    OTHER = "OTHER"


class TimeOfDay(str, Enum):
    DAY = "DAY"
    NIGHT = "NIGHT"
    DUSK = "DUSK"
    DAWN = "DAWN"
    CONTINUOUS = "CONTINUOUS"
    SAME = "SAME"
    UNKNOWN = "UNKNOWN"


class ProductionDependency(BaseModel):
    """Represents a prerequisite or technical dependency required before/during scene shooting."""
    dependency_type: str = Field(..., description="Category of dependency (e.g., Equipment, Stunt, Permit, Crew, Art)")
    description: str = Field(..., description="Detailed description of the dependency requirement")
    required_by_department: Optional[str] = Field(default=None, description="Department responsible (e.g., Camera, SFX, Props, Logistics)")


class ProductionRisk(BaseModel):
    """Represents a potential risk during scene production along with risk category and mitigation."""
    risk_category: str = Field(..., description="Category of risk (e.g., Safety, Weather, Time, Cost, Technical)")
    description: str = Field(..., description="Detailed explanation of the risk")
    severity: str = Field(default="MEDIUM", description="Severity level: LOW, MEDIUM, HIGH, CRITICAL")
    mitigation_notes: Optional[str] = Field(default=None, description="Recommended steps to mitigate the risk")


class SceneAnalysis(BaseModel):
    """
    Complete structured production analysis for a single screenplay scene.
    Covers all 11 required production parameters.
    """
    scene_number: str = Field(..., description="Scene identifier string or number, e.g. '1' or '2A'")
    scene_description: str = Field(..., description="Summary of narrative action and context occurring in the scene")
    location_type: SceneLocationType = Field(..., description="Interior/Exterior setting indicator (INT, EXT, INT/EXT, OTHER)")
    location_name: str = Field(..., description="Name or setting of the location, e.g., 'WAREHOUSE - MAIN FLOOR'")
    time_of_day: TimeOfDay = Field(..., description="Lighting / time requirement (DAY, NIGHT, DUSK, DAWN, CONTINUOUS, etc.)")
    characters: List[str] = Field(default_factory=list, description="List of character names present in the scene")
    props: List[str] = Field(default_factory=list, description="Key props featured or handled in the scene")
    weather_environment: List[str] = Field(default_factory=list, description="Atmospheric or weather requirements, e.g., 'Heavy Rain', 'Smoke/Fog'")
    special_production_requirements: List[str] = Field(default_factory=list, description="Special effects, stunts, camera rigs, or audio requirements")
    production_dependencies: List[ProductionDependency] = Field(default_factory=list, description="Dependencies required prior to shooting")
    potential_production_risks: List[ProductionRisk] = Field(default_factory=list, description="Identified hazards or operational risks")
