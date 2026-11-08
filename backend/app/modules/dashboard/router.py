from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_db
from app.core.security import get_current_user
from app.db.models.user import User
from app.modules.dashboard.schemas import DashboardOverviewResponse
from app.modules.dashboard.services.dashboard_service import get_dashboard_overview

router = APIRouter(prefix="/dashboard", tags=["Dashboard"])


@router.get(
    "/overview",
    response_model=DashboardOverviewResponse,
    status_code=status.HTTP_200_OK,
    summary="Retrieve unified dashboard analytics and live performance charts.",
)
async def get_overview(
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """
    Fetch comprehensive dashboard metrics, comparison bar charts,
    weekly skill trends, activity calendar, and unified assessment history.
    """
    return await get_dashboard_overview(db=db, user_id=current_user.id)
