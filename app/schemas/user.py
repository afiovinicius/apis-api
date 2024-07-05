import uuid
from datetime import datetime
from typing import Optional

from pydantic import BaseModel, EmailStr


class UserBase(BaseModel):
    email: EmailStr
    name: str


class UserCreate(UserBase):
    password: str
    role: str
    is_provider_auth: str = "email"


class UserUpdate(BaseModel):
    is_active: Optional[bool] = None
    role: Optional[str] = None


class UserInDB(UserBase):
    id: uuid.UUID
    is_active: bool
    role: str
    is_provider_auth: str
    created_at: datetime
    updated_at: datetime


class User(UserInDB):
    pass
