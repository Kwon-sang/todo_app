from typing import Optional, Annotated, ClassVar, Any

from pydantic import EmailStr, BaseModel
from sqlmodel import SQLModel, Field

from utils import bcrypt_context


class User(SQLModel, table=True):
    __tablename__ = 'users'

    id: Optional[int] = Field(primary_key=True, default=None)
    username: str = Field(unique=True, index=True, min_length=4)
    password: str = Field(min_length=4)
    email: str = Field(unique=True)
    role: str = Field(default='basic')
    is_active: bool = Field(default=True)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.password = self.encrypt_password(self.password)

    def encrypt_password(self, raw_password):
        return bcrypt_context.hash(raw_password)

    def update(self, **kwargs):
        for key, value in kwargs.items():
            setattr(self, key, value)


class UserCreateReqeust(BaseModel):
    username: str
    password: str
    email: Optional[EmailStr] = None


class UserUpdateRequest(BaseModel):
    email: Optional[EmailStr] = None


class UserPasswordChangeRequest(BaseModel):
    password: str
    new_password: str
