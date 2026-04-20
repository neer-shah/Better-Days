from typing import cast
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.api.deps import get_current_user
from app.db.session import get_db
from app.models.user import User
from app.schemas.checkin import CheckinCreate, CheckinResponse, CheckinUpdate
from app.services.checkin_service import (
    get_checkin_by_user_and_date,
    create_checkin,
    get_user_checkins,
    get_checkin_by_id_for_user,
    update_checkin,
)

router = APIRouter(prefix="/checkins", tags=["checkins"])


@router.post("/", response_model=CheckinResponse, status_code=status.HTTP_201_CREATED)
def create_daily_checkin(
    checkin_data: CheckinCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    user_id = cast(int, current_user.id)

    existing_checkin = get_checkin_by_user_and_date(
        db=db,
        user_id=user_id,
        checkin_date=checkin_data.date,
    )

    if existing_checkin is not None:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="You already have a check-in for today",
        )

    return create_checkin(
        db=db,
        user_id=user_id,
        checkin_data=checkin_data,
    )


@router.get("/", response_model=list[CheckinResponse])
def read_user_checkins(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return get_user_checkins(db=db, user_id=cast(int, current_user.id))


@router.put("/{checkin_id}", response_model=CheckinResponse)
def update_user_checkin(
    checkin_id: int,
    checkin_data: CheckinUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    user_id = cast(int, current_user.id)

    existing_checkin = get_checkin_by_id_for_user(
        db=db,
        user_id=user_id,
        checkin_id=checkin_id,
    )

    if existing_checkin is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Check-in not found.",
        )

    conflicting_checkin = get_checkin_by_user_and_date(
        db=db,
        user_id=user_id,
        checkin_date=checkin_data.date,
    )

    if (
        conflicting_checkin is not None
        and cast(int, conflicting_checkin.id) != cast(int, existing_checkin.id)
    ):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="You already have another check-in for this date.",
        )

    return update_checkin(
        db=db,
        checkin=existing_checkin,
        checkin_data=checkin_data,
    )
