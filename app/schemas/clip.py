from typing import Optional
from pydantic import BaseModel, ConfigDict, Field


class ClipCreate(BaseModel):
    title: str = Field(..., min_length=1, max_length=255)
    description: Optional[str] = Field(None, max_length=500)
    genre: str = Field(..., min_length=1, max_length=100)
    duration: float = Field(..., gt=0)
    audio_url: str = Field(..., min_length=5, max_length=1000)


class ClipResponse(BaseModel):
    id: int
    title: str
    description: Optional[str] = None
    genre: str
    duration: float
    audio_url: str
    play_count: int

    model_config = ConfigDict(from_attributes=True)


class ClipStatsResponse(BaseModel):
    id: int
    title: str
    play_count: int

    model_config = ConfigDict(from_attributes=True)