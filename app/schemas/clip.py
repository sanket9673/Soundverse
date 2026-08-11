from typing import Optional
from pydantic import BaseModel, ConfigDict


class ClipResponse(BaseModel):
    id: int
    title: str
    description: Optional[str] = None
    genre: str
    duration: float
    audio_url: str
    play_count: int

    model_config = ConfigDict(from_attributes=True)