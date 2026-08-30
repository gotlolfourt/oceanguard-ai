from sqlalchemy import text
from sqlalchemy.orm import Session
from fastapi import APIRouter, Depends

from app.core.errors import success_response
from app.database import get_db

router = APIRouter(prefix="/health", tags=["health"])


@router.get("")
async def detailed_health(db: Session = Depends(get_db)):
    db.execute(text("SELECT 1"))
    return success_response({"service": "backend", "database": "ok"})
