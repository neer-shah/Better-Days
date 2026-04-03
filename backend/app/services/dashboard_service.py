from sqlalchemy.orm import Session
from sqlalchemy import func

from app.models.daily_checkin import DailyCheckin


def get_dashboard_summary(db: Session, user_id: int):
    result = (
        db.query(
            func.count(DailyCheckin.id),
            func.avg(DailyCheckin.mood),
            func.avg(DailyCheckin.stress),
            func.avg(DailyCheckin.sleep_hours),
            func.max(DailyCheckin.date),
        )
        .filter(DailyCheckin.user_id == user_id)
        .first()
    )

    if result is None:
        return {
            "total_checkins": 0,
            "average_mood": None,
            "average_stress": None,
            "average_sleep_hours": None,
            "latest_checkin_date": None,
        }

    total_checkins, avg_mood, avg_stress, avg_sleep, latest_date = result

    return {
        "total_checkins": total_checkins or 0,
        "average_mood": round(float(avg_mood), 2) if avg_mood is not None else None,
        "average_stress": round(float(avg_stress), 2) if avg_stress is not None else None,
        "average_sleep_hours": round(float(avg_sleep), 2) if avg_sleep is not None else None,
        "latest_checkin_date": latest_date,
    }


def get_dashboard_trends(db: Session, user_id: int):
    checkins = (
        db.query(DailyCheckin)
        .filter(DailyCheckin.user_id == user_id)
        .order_by(DailyCheckin.date.asc())
        .all()
    )

    return [
        {
            "date": checkin.date,
            "mood": checkin.mood,
            "stress": checkin.stress,
            "energy": checkin.energy,
            "sleep_hours": checkin.sleep_hours,
            "productivity": checkin.productivity,
        }
        for checkin in checkins
    ]


def get_recent_checkins(db: Session, user_id: int, limit: int = 5):
    return (
        db.query(DailyCheckin)
        .filter(DailyCheckin.user_id == user_id)
        .order_by(DailyCheckin.date.desc())
        .limit(limit)
        .all()
    )


def get_dashboard_data(db: Session, user_id: int):
    summary = get_dashboard_summary(db, user_id)
    trends = get_dashboard_trends(db, user_id)
    recent_checkins = get_recent_checkins(db, user_id)

    return {
        "summary": summary,
        "trends": trends,
        "recent_checkins": recent_checkins,
    }
