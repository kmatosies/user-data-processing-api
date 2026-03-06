from sqlalchemy.orm import Session
from sqlalchemy import select
from ..db.models.user import User


class UserRepository:
    def get_by_id(self, db: Session, user_id: str) -> User | None:
        return db.scalar(select(User).where(User.id == user_id))

    def bulk_upsert(self, db: Session, rows: list[dict]) -> tuple[int, int]:
        """Insert rows that don't exist yet. Perform a single query to find existing IDs to avoid N+1 queries."""
        inserted = 0
        skipped = 0

        if not rows:
            return 0, 0

        ids = [r["id"] for r in rows]
        existing_ids = set(db.scalars(select(User.id).where(User.id.in_(ids))).all())

        for r in rows:
            if r["id"] in existing_ids:
                skipped += 1
                continue
            db.add(User(**r))
            inserted += 1

        return inserted, skipped
