from fastapi import Depends
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from sqlalchemy.orm import Session

from app.core.errors import AppError
from app.core.security import decode_token
from app.database import get_db
from app.models import User

bearer_scheme = HTTPBearer(auto_error=False)


def get_current_user(
    credentials: HTTPAuthorizationCredentials | None = Depends(bearer_scheme),
    db: Session = Depends(get_db),
) -> User:
    if credentials is None:
        raise AppError(401, "Missing authorization token")

    payload = decode_token(credentials.credentials)
    if payload.get("type") != "access":
        raise AppError(401, "Invalid token type")

    user = db.get(User, payload.get("user_id"))
    if not user or not user.is_active:
        raise AppError(401, "User not found or inactive")

    return user


def require_admin(current_user: User = Depends(get_current_user)) -> User:
    if current_user.role.name != "admin":
        raise AppError(403, "Admin permissions required")
    return current_user
