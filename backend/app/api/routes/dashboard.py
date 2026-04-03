from typing import cast

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.api.deps import get_current_user
from app.db.session import get_db
from app.models.user import User
from app.schemas.dashboard import DashboardResponse
from app.services.dashboard_service import get_dashboard_data

router = APIRouter(prefix="/dashboard", tags=["dashboard"])

@router.get("/", response_model=DashboardResponse)
def read_dashboard(db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    user_id = cast(int, current_user.id)
    return get_dashboard_data(db=db, user_id=user_id)
