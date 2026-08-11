from typing import List
import anyio
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.responses import StreamingResponse
from sqlalchemy.orm import Session
import httpx

from app.core.database import get_db
from app.core.security import verify_api_key
from app.monitoring.metrics import STREAM_COUNTER
from app.schemas.clip import ClipCreate, ClipResponse, ClipStatsResponse
from app.services import clip_service

router = APIRouter(
    prefix="/play",
    tags=["Play"],
    dependencies=[Depends(verify_api_key)],
)


@router.get("", response_model=List[ClipResponse])
def get_clips(db: Session = Depends(get_db)):
    return clip_service.get_all_clips(db)


@router.post("", response_model=ClipResponse, status_code=status.HTTP_201_CREATED)
def create_clip(clip_in: ClipCreate, db: Session = Depends(get_db)):
    return clip_service.create_clip(db, clip_in)


@router.get("/{clip_id}/stream")
async def stream_clip(clip_id: int, db: Session = Depends(get_db)):
    clip = await anyio.to_thread.run_sync(clip_service.get_clip_by_id, db, clip_id)
    if not clip:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Clip not found",
        )

    await anyio.to_thread.run_sync(clip_service.increment_play_count, db, clip)
    STREAM_COUNTER.labels(clip_id=str(clip.id), title=clip.title).inc()

    async def iterfile():
        async with httpx.AsyncClient(follow_redirects=True) as client:
            async with client.stream("GET", clip.audio_url) as response:
                response.raise_for_status()
                async for chunk in response.aiter_bytes():
                    yield chunk

    return StreamingResponse(iterfile(), media_type="audio/mpeg")


@router.get("/{clip_id}/stats", response_model=ClipStatsResponse)
def get_clip_stats(clip_id: int, db: Session = Depends(get_db)):
    clip = clip_service.get_clip_by_id(db, clip_id)
    if not clip:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Clip not found",
        )
    return clip