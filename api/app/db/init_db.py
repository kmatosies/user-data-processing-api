from .session import engine
from .base import Base
from .models.user import User


def init_db():
    """Create database tables (safe to call on startup)."""
    Base.metadata.create_all(bind=engine)
