from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.api.deps import get_current_user
from app.core.errors import AppError, success_response
from app.core.security import (
    create_access_token,
    create_refresh_token,
    decode_token,
    hash_password,
    verify_password,
)
from app.database import get_db
from app.models import Role, User
from app.schemas import LoginRequest, LogoutRequest, RefreshRequest, RegisterRequest

router = APIRouter(prefix="/auth", tags=["auth"])


def _is_strong_password(password: str) -> bool:
    return (
        len(password) >= 8
        and any(ch.islower() for ch in password)
        and any(ch.isdigit() for ch in password)
    )


@router.post("/register", status_code=201)
async def register(payload: RegisterRequest, db: Session = Depends(get_db)):
    existing = db.query(User).filter(User.email == payload.email).first()
    if existing:
        raise AppError(409, "Email already in use")

    if not _is_strong_password(payload.password):
        raise AppError(400, "Password must include letters and numbers")

    role = db.query(Role).filter(Role.name == "field_operator").first()
    if role is None:
        raise AppError(500, "Default role not configured")

    user = User(
        email=payload.email,
        password_hash=hash_password(payload.password),
        first_name=payload.first_name,
        last_name=payload.last_name,
        role_id=role.id,
        organization_id=1,
        is_active=True,
    )
    db.add(user)
    db.commit()
    db.refresh(user)

    role_name = user.role.name if user.role else "field_operator"
    tokens = {
        "access_token": create_access_token(user.id, user.email, role_name),
        "refresh_token": create_refresh_token(user.id, user.email, role_name),
        "token_type": "bearer",
    }
    return success_response(tokens, status=201)


@router.post("/login")
async def login(payload: LoginRequest, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.email == payload.email).first()
    if user is None or not verify_password(payload.password, user.password_hash):
        raise AppError(401, "Invalid email or password")

    role_name = user.role.name if user.role else "operator"
    tokens = {
        "access_token": create_access_token(user.id, user.email, role_name),
        "refresh_token": create_refresh_token(user.id, user.email, role_name),
        "token_type": "bearer",
    }
    return success_response(tokens)


@router.post("/refresh")
async def refresh(payload: RefreshRequest):
    token_data = decode_token(payload.refresh_token)
    if token_data.get("type") != "refresh":
        raise AppError(401, "Invalid refresh token")

    access_token = create_access_token(token_data["user_id"], token_data["email"], token_data["role"])
    return success_response({"access_token": access_token, "token_type": "bearer"})


@router.post("/logout")
async def logout(_: LogoutRequest, __: User = Depends(get_current_user)):
    return success_response({"message": "Logged out"})
