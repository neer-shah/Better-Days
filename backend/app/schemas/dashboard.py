from datetime import date
from pydantic import BaseModel

class DashboardSummary(BaseModel):
    total_checkins: int
    average_mood: float | None
    average_stress: float | None
    average_sleep_hours: float | None
    latest_checkin_date: date | None

class DashboardTrendPoint(BaseModel):
    date: date
    mood: int
    stress: int
    sleep_hours: float
    productivity: int

class RecentCheckinItem(BaseModel):
    id: int
    date: date
    mood: int
    stress: int
    energy: int
    small_win: str

    class Config:
        from_attributes = True

class DashboardResponse(BaseModel):
    summary: DashboardSummary
    trends: list[DashboardTrendPoint]
    recent_checkins: list[RecentCheckinItem]