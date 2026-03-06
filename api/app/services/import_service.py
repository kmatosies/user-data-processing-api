import io
import requests
import ijson
from sqlalchemy.orm import Session
from fastapi import HTTPException

from ..repositories.user_repository import UserRepository


class ImportService:
    def __init__(self):
        self.repo = UserRepository()

    def import_from_url(self, db: Session, url: str, batch_size: int = 1000) -> dict:
        """Stream-import users from a JSON URL. Expects a top-level array of items."""
        try:
            resp = requests.get(url, stream=True, timeout=60)
        except requests.RequestException as e:
            raise HTTPException(
                status_code=400, detail=f"Failed to fetch URL: {str(e)}"
            )

        if resp.status_code != 200:
            raise HTTPException(
                status_code=400, detail=f"URL returned status {resp.status_code}"
            )

        content_type = resp.headers.get("Content-Type", "")
        if (
            "json" not in content_type
            and "application/octet-stream" not in content_type
        ):
            raise HTTPException(
                status_code=400, detail="URL did not return JSON content"
            )

        inserted_total = 0
        skipped_total = 0
        invalid_total = 0

        try:
            parser = ijson.items(resp.raw, "item")
        except Exception:
            raise HTTPException(status_code=400, detail="Invalid JSON stream")

        batch: list[dict] = []

        for obj in parser:
            row = self._extract_user_row(obj)
            if row is None:
                invalid_total += 1
                continue

            batch.append(row)

            if len(batch) >= batch_size:
                ins, skp = self._persist_batch(db, batch)
                inserted_total += ins
                skipped_total += skp
                batch.clear()

        if batch:
            ins, skp = self._persist_batch(db, batch)
            inserted_total += ins
            skipped_total += skp

        return {
            "status": "ok",
            "inserted": inserted_total,
            "skipped": skipped_total,
            "invalid": invalid_total,
        }

    def _extract_user_row(self, obj: dict) -> dict | None:
        """Map incoming JSON object to storage dict. Expects `_id`, `first_name`, `last_name`, `email`."""
        user_id = obj.get("_id")
        first_name = obj.get("first_name")
        last_name = obj.get("last_name")
        email = obj.get("email")

        if not user_id or not first_name or not last_name or not email:
            return None

        return {
            "id": str(user_id),
            "first_name": str(first_name),
            "last_name": str(last_name),
            "email": str(email),
        }

    def _persist_batch(self, db: Session, batch: list[dict]) -> tuple[int, int]:
        try:
            inserted, skipped = self.repo.bulk_upsert(db, batch)
            db.commit()
            return inserted, skipped
        except Exception as e:
            db.rollback()
            raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")
