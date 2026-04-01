from sqlalchemy import Column, Integer, Float, Boolean, Date, DateTime, ForeignKey, String, Text, UniqueConstraint
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship

from app.db.session import Base

class DailyCheckins(Base):
    __tablename__ = "daily_checkins"

    __table_args__ = (
        UniqueConstraint("user_id", "date", name="uq_user_checkin_date"),
    )

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)

    date = Column(Date, nullable=False)

    mood = Column(Integer, nullable=False)
    stress = Column(Integer, nullable=False)
    energy = Column(Integer, nullable=False)
    sleep_hours = Column(Float, nullable=False)
    exercise_done = Column(Boolean, nullable=False)
    social_connection = Column(Integer, nullable=False)
    productivity = Column(Integer, nullable=False)
    small_wim = Column(String, nullable=False)

    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)

    user = relationship("User", back_populates="checkins")