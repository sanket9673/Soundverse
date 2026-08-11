from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.schemas.clip import ClipResponse
from app.services.clip_service import get_all_clips

router = APIRouter(prefix="/play", tags=["Play"])


@router.get("", response_model=list[ClipResponse])
@router.get("/", response_model=list[ClipResponse], include_in_schema=False)
def list_clips(db: Session = Depends(get_db)) -> list[ClipResponse]:
    """Fetch all available audio clips with metadata."""
    clips = get_all_clips(db)
    return list(clips)