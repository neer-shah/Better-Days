from datetime import datetime, date
from pydantic import BaseModel, Field

class CheckinCreate(BaseModel):
    date: date
    mood: int = Field(ge=1, le=5)
    stress: int = Field(ge=1, le=5)
    energy: int = Field(ge=1, le=5)
    sleep_hours: float = Field(ge=0, le=24)
    exercise_done: bool
    social_connection: int = Field(ge=1, le=5)
    productivity: int = Field(ge=1, le=5)
    small_win: str

class CheckinResponse(BaseModel):
    id: int
    user_id: int
    date: date
    mood: int
    stress: int
    energy: int
    sleep_hours: float
    exercise_done: bool
    social_connection: int
    productivity: int
    small_win: str

class Config:
    from_attributes = True
