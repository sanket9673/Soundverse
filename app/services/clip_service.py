from typing import List, Optional
from sqlalchemy.orm import Session

from app.models.clip import Clip
from app.schemas.clip import ClipCreate


def get_all_clips(db: Session) -> List[Clip]:
    """Fetch all audio clips from the database."""
    return db.query(Clip).all()


def get_clip_by_id(db: Session, clip_id: int) -> Optional[Clip]:
    """Fetch a single audio clip by primary key ID."""
    return db.query(Clip).filter(Clip.id == clip_id).first()


def increment_play_count(db: Session, clip: Clip) -> Clip:
    """Increment the play_count for a clip atomically and commit to the database."""
    db.query(Clip).filter(Clip.id == clip.id).update({Clip.play_count: Clip.play_count + 1}, synchronize_session="evaluate")
    db.commit()
    db.refresh(clip)
    return clip


def create_clip(db: Session, clip_data: ClipCreate) -> Clip:
    """Create a new audio clip record in the database."""
    clip = Clip(**clip_data.model_dump())
    db.add(clip)
    db.commit()
    db.refresh(clip)
    return clip