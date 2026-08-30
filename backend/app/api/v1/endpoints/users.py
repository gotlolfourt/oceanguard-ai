from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.api.deps import get_current_user, require_admin
from app.core.errors import success_response
from app.database import get_db
from app.models import User
from app.schemas import UpdateMeRequest

router = APIRouter(prefix="/users", tags=["users"])


def _serialize(user: User) -> dict:
    return {
        "id": user.id,
        "email": user.email,
        "first_name": user.first_name,
        "last_name": user.last_name,
        "role": user.role.name if user.role else "unknown",
        "organization": user.organization.name if user.organization else "unknown",
        "is_active": user.is_active,
    }


@router.get("/me")
async def me(current_user: User = Depends(get_current_user)):
    return success_response(_serialize(current_user))


@router.put("/me")
async def update_me(payload: UpdateMeRequest, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    if payload.first_name is not None:
        current_user.first_name = payload.first_name
    if payload.last_name is not None:
        current_user.last_name = payload.last_name
    db.add(current_user)
    db.commit()
    db.refresh(current_user)
    return success_response(_serialize(current_user))


@router.get("")
async def list_users(_: User = Depends(require_admin), db: Session = Depends(get_db)):
    users = db.query(User).all()
    return success_response([_serialize(user) for user in users])
