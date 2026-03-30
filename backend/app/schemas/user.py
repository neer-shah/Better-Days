from pydantic import BaseModel, EmailStr, Field
from datetime import datetime

class UserCreate(BaseModel):
    name: str
    email: EmailStr
    password: str = Field(min_length=8, max_length=72)

class UserResponse(BaseModel):
    id: int
    name: str
    email: EmailStr
    anonymous_name: str
    created_at: datetime

    class Config:
        from_attributes = True
