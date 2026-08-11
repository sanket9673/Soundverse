from typing import List, Optional
from sqlalchemy.orm import Session
from app.models.clip import Clip


def get_all_clips(db: Session) -> List[Clip]:
    """Fetch all audio clips from the database."""
    return db.query(Clip).all()


def get_clip_by_id(db: Session, clip_id: int) -> Optional[Clip]:
    """Fetch a single audio clip by primary key ID."""
    return db.query(Clip).filter(Clip.id == clip_id).first()


def increment_play_count(db: Session, clip: Clip) -> Clip:
    """Increment the play_count for a clip and commit to the database."""
    clip.play_count += 1
    db.commit()
    db.refresh(clip)
    return clip