import logging
import sys
from sqlalchemy.orm import Session

from app.core.database import Base, SessionLocal, engine
from app.models.clip import Clip

logging.basicConfig(level=logging.INFO, format="%(levelname)s: %(message)s")
logger = logging.getLogger(__name__)

INITIAL_CLIPS = [
    {
        "title": "Acoustic Breeze",
        "description": "Relaxing acoustic guitar melody for background listening",
        "genre": "Acoustic",
        "duration": 157.0,
        "audio_url": "https://www.soundhelix.com/examples/mp3/SoundHelix-Song-1.mp3",
    },
    {
        "title": "Electronic Beats",
        "description": "Upbeat energetic electronic synth track",
        "genre": "Electronic",
        "duration": 210.0,
        "audio_url": "https://www.soundhelix.com/examples/mp3/SoundHelix-Song-2.mp3",
    },
    {
        "title": "Jazz Groove",
        "description": "Smooth jazz saxophone and bass vibe",
        "genre": "Jazz",
        "duration": 180.0,
        "audio_url": "https://www.soundhelix.com/examples/mp3/SoundHelix-Song-3.mp3",
    },
    {
        "title": "Ambient Relax",
        "description": "Calm atmospheric ambient synth pads",
        "genre": "Ambient",
        "duration": 240.0,
        "audio_url": "https://www.soundhelix.com/examples/mp3/SoundHelix-Song-4.mp3",
    },
    {
        "title": "Rock Riff",
        "description": "High-energy classic rock guitar riff",
        "genre": "Rock",
        "duration": 195.0,
        "audio_url": "https://www.soundhelix.com/examples/mp3/SoundHelix-Song-5.mp3",
    },
    {
        "title": "Chill Hop",
        "description": "Lo-fi chill hip-hop beat for studying and focus",
        "genre": "Lo-Fi",
        "duration": 165.0,
        "audio_url": "https://www.soundhelix.com/examples/mp3/SoundHelix-Song-6.mp3",
    },
]


def seed_database() -> None:
    # Ensure database schema is created
    Base.metadata.create_all(bind=engine)

    session: Session = SessionLocal()
    try:
        # Check if database already has clips
        existing_count = session.query(Clip).count()
        if existing_count > 0:
            logger.info("Database already seeded. Skipping insertion.")
            return

        # Seed initial audio clips
        clips = [Clip(**clip_data) for clip_data in INITIAL_CLIPS]
        session.add_all(clips)
        session.commit()
        logger.info(f"Successfully seeded database with {len(clips)} audio clips.")
    except Exception as e:
        session.rollback()
        logger.error(f"Failed to seed database: {e}")
        sys.exit(1)
    finally:
        session.close()


if __name__ == "__main__":
    seed_database()