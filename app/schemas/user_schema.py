from pydantic import BaseModel, Field, field_validator
from typing import Annotated
from enum import Enum

class UserRole(str, Enum):
    USER = "user"
    ADMIN = "admin"

class UserRegister(BaseModel):
    username: Annotated[str, Field(min_length=3, max_length=50)]
    password: Annotated[str, Field(min_length=6)]
    confirm_password: str
    role: UserRole = UserRole.USER

    @field_validator("confirm_password")
    @classmethod
    def passwords_match(cls, v, info):
        if "password" in info.data and v != info.data["password"]:
            raise ValueError("Passwords do not match")
        return v