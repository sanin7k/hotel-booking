from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from backend.app.database.database import get_db
from backend.app.models.models import User
from backend.app.schemas.schemas import UserProfile
from backend.app.utils.role_checker import require_role

router = APIRouter(prefix="/admin", tags=["Admin"])

@router.get("/users", response_model=list[UserProfile], dependencies=[Depends(require_role("admin"))])
def get_all_users(db: Session = Depends(get_db)):
    users = db.query(User).all()
    return users
