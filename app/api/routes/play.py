from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.responses import StreamingResponse
from sqlalchemy.orm import Session
import httpx

from app.core.database import get_db
from app.schemas.clip import ClipResponse, ClipStatsResponse
from app.services import clip_service

router = APIRouter(prefix="/play", tags=["play"])


@router.get("", response_model=List[ClipResponse])
def get_clips(db: Session = Depends(get_db)):
    """Return all dummy sound clips."""
    return clip_service.get_all_clips(db)


@router.get("/{clip_id}/stream")
async def stream_clip(clip_id: int, db: Session = Depends(get_db)):
    """Stream clip audio from public URL and increment play_count."""
    clip = clip_service.get_clip_by_id(db, clip_id)
    if not clip:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Clip not found",
        )

    # Increment play count on DB before streaming
    clip_service.increment_play_count(db, clip)

    # Stream audio bytes asynchronously from remote audio_url
    async def iterfile():
        async with httpx.AsyncClient(follow_redirects=True) as client:
            async with client.stream("GET", clip.audio_url) as response:
                response.raise_for_status()
                async for chunk in response.aiter_bytes():
                    yield chunk

    return StreamingResponse(iterfile(), media_type="audio/mpeg")


@router.get("/{clip_id}/stats", response_model=ClipStatsResponse)
def get_clip_stats(clip_id: int, db: Session = Depends(get_db)):
    """Return play count and metadata for a given clip."""
    clip = clip_service.get_clip_by_id(db, clip_id)
    if not clip:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Clip not found",
        )
    return clip