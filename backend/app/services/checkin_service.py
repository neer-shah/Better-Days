from datetime import date
from sqlalchemy.orm import Session

from app.models.daily_checkin import DailyCheckin

def get_checkin_by_user_and_date(db: Session, user_id: int, checkin_date: date):
    return (
        db.query(DailyCheckin).filter(
            DailyCheckin.user_id == user_id,
            DailyCheckin.date == checkin_date
        ).first()
    )

def create_checkin(db: Session, user_id: int, checkin_data) -> DailyCheckin:
    checkin = DailyCheckin(
        user_id=user_id,
        date=checkin_data.date,
        mood=checkin_data.mood,
        stress=checkin_data.stress,
        energy=checkin_data.energy,
        sleep_hours=checkin_data.sleep_hours,
        exercise_done=checkin_data.exercise_done,
        social_connection=checkin_data.social_connection,
        productivity=checkin_data.productivity,
        small_win=checkin_data.small_win
    )

    db.add(checkin)
    db.commit()
    db.refresh(checkin)
    return checkin

def get_user_checkins(db: Session, user_id: int):
    return (
        db.query(DailyCheckin)
        .filter(DailyCheckin.user_id == user_id)
        .order_by(DailyCheckin.date.desc())
        .all()
    )
