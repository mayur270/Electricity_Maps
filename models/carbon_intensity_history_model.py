"""Pydantic Data Validation Models"""

from dataclasses import dataclass
from datetime import datetime
from typing import List, Optional

from pydantic import BaseModel, Field


@dataclass(kw_only=True)
class CarbonIntensity(BaseModel):
    """Carbon intensity model."""

    zone: str
    carbon_intensity: int = Field(alias="carbonIntensity")
    datetime: datetime
    updated_at: datetime = Field(alias="updatedAt")
    created_at: datetime = Field(alias="createdAt")
    emission_factor_type: Optional[str] = Field(alias="emissionFactorType")
    is_estimated: bool = Field(alias="isEstimated")
    estimation_method: Optional[str] = Field(alias="estimationMethod")


@dataclass(kw_only=True)
class CarbonIntensityHistory(BaseModel):
    """Carbon intensity history model."""

    zone: str
    history: List[CarbonIntensity]


@dataclass(kw_only=True)
class ZoneParam:
    """Zone param model."""

    zone: str


@dataclass(kw_only=True)
class CoordinatesParam:
    """Coordinates param model."""

    lat: str
    lon: str
