from typing import Optional
from sqlalchemy import Float, Integer, String
from sqlalchemy.orm import Mapped, mapped_column

from app.core.database import Base


class Clip(Base):
    __tablename__ = "clips"

    id: Mapped[int] = mapped_column(
        Integer, primary_key=True, index=True, autoincrement=True
    )
    title: Mapped[str] = mapped_column(String(255), nullable=False)
    description: Mapped[Optional[str]] = mapped_column(
        String(500), nullable=True
    )
    genre: Mapped[str] = mapped_column(String(100), nullable=False, index=True)
    duration: Mapped[float] = mapped_column(Float, nullable=False)
    audio_url: Mapped[str] = mapped_column(String(1000), nullable=False)
    play_count: Mapped[int] = mapped_column(
        Integer, default=0, nullable=False
    )