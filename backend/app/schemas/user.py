from pydantic import BaseModel, EmailStr


class UserOut(BaseModel):
    id: str
    email: EmailStr
    first_name: str
    last_name: str
    role: str
    organization: str
    is_active: bool


class UpdateMeRequest(BaseModel):
    first_name: str | None = None
    last_name: str | None = None
