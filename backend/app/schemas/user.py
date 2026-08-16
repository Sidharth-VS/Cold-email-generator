from pydantic import BaseModel, ConfigDict
from datetime import datetime
import uuid


class UserBase(BaseModel):
    email: str
    username: str
    is_active: bool = True
    is_superuser: bool = False


class UserCreate(UserBase):
    hashed_password: str


class UserUpdate(BaseModel):
    email: str | None = None
    username: str | None = None
    hashed_password: str | None = None
    is_active: bool | None = None
    is_superuser: bool | None = None


class UserResponse(UserBase):
    model_config = ConfigDict(from_attributes=True)

    id: uuid.UUID
    created_at: datetime
    updated_at: datetime
