from typing import cast
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.api.deps import get_current_user
from app.db.session import get_db
from app.models.user import User
from app.schemas.checkin import CheckinCreate, CheckinResponse
from app.services.checkin_service import get_checkin_by_user_and_date, create_checkin, get_user_checkins

router = APIRouter(prefix="/checkins", tags=["checkins"])

@router.post("/", response_model=CheckinResponse, status_code=status.HTTP_201_CREATED)
def create_daily_checkin(checkin_data: CheckinCreate, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    existing_checkin = get_checkin_by_user_and_date(
        db=db,
        user_id=cast(int, current_user.id),
        checkin_date=checkin_data.date
    )

    if existing_checkin:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="You already have a check-in for today"
        )
    
    return create_checkin(
        db=db,
        user_id=cast(int, current_user.id),
        checkin_data=checkin_data
    )

@router.get("/", response_model=list[CheckinResponse])
def read_user_checkins(db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    return get_user_checkins(db=db, user_id=cast(int, current_user.id))
