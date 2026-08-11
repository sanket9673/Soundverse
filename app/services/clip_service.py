from typing import Sequence
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.clip import Clip


def get_all_clips(db: Session) -> Sequence[Clip]:
    """Retrieve all audio clips from the database."""
    return db.scalars(select(Clip)).all()