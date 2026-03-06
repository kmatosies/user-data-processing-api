from fastapi import APIRouter, Depends, Form, HTTPException
from sqlalchemy.orm import Session

from ..db.session import get_db
from ..repositories.user_repository import UserRepository
from ..services.import_service import ImportService

router = APIRouter(prefix="/api/v1", tags=["users"])

repo = UserRepository()
import_service = ImportService()


@router.post("/import/users")
def import_users(url: str = Form(...), db: Session = Depends(get_db)):
    """
    Recebe URL via form-data:
      url=https://.../users.json
    """
    if not url.startswith("http"):
        raise HTTPException(status_code=422, detail="url must start with http/https")

    return import_service.import_from_url(db, url)


@router.get("/users/{user_id}")
def get_user(user_id: str, db: Session = Depends(get_db)):
    user = repo.get_by_id(db, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    return {
        "user": {
            "id": user.id,
            "first_name": user.first_name,
            "last_name": user.last_name,
            "email": user.email,
        }
    }
