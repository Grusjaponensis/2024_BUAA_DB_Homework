import uuid, math
from datetime import datetime, timedelta
from typing import Any

from fastapi import (
    APIRouter, Depends, HTTPException, status, Query
)
from fastapi.responses import JSONResponse
from sqlmodel import func, select

from app.api.deps import (
    CurrentUser,
    LoginRequired,
    SessionDep,
    get_current_superuser
)
from app.models.donation import Donation, DonationCreate, DonationPublic
from app.core.config import settings


router = APIRouter()


@router.get("/total")
async def get_donations_total(
    session: SessionDep,
    start_date: str = Query(None, description="Start date in format YYYY-MM-DD"),
    end_date: str = Query(None, description="End date in format YYYY-MM-DD")
) -> dict[str, Any]:
    """
    Get total donations by date range.
    """
    try:
        start = datetime.strptime(start_date, '%Y-%m-%d') if start_date else None
        end = datetime.strptime(end_date, '%Y-%m-%d') if end_date else None
    except ValueError:
        raise HTTPException(status_code=400, detail="Invalid date format. Use 'YYYY-MM-DD'.")
    
    today = datetime.now(settings.UTC_8).replace(hour=0, minute=0, second=0, microsecond=0) + timedelta(days=1) - timedelta(seconds=1)
    
    if not end:
        end = today
    if not start:
        start = end - timedelta(days=30)
    
    # NOTE: beware of this clause
    donations = session.exec(
        select(func.date(Donation.donated_at), func.sum(Donation.amount), func.count(Donation.id))
            .where(Donation.donated_at >= start)
            .where(Donation.donated_at <= end)
            .group_by(func.date(Donation.donated_at))
            .order_by(func.date(Donation.donated_at))
    ).all()

    total_amount = session.exec(
        select(func.sum(Donation.amount))
        .where(Donation.donated_at >= start)
        .where(Donation.donated_at <= end)
    ).one_or_none()

    aggregated_data = [
        {"date": donation[0], "amount": donation[1] or 0, "count": donation[2] or 0}
        for donation in donations
    ]

    return {
        "total_amount": round(total_amount, 2) if total_amount else 0,
        "aggregated_data": aggregated_data
    }


@router.get("/", response_model=list[DonationPublic], dependencies=[LoginRequired])
async def get_donations(
    session: SessionDep, 
    offset: int = 0,
    limit: int = 100
): 
    """
    Get all donations.
    """
    donations = session.exec(
        select(Donation)
            .offset(offset).limit(limit)
            .order_by(Donation.donated_at.desc())
    ).all()

    response = [DonationPublic.model_validate(donation.model_dump()) for donation in donations]
    return response
    
    
@router.post("/", response_model=DonationPublic)
async def create_donation(
    session: SessionDep,
    current_user: CurrentUser,
    donation_in: DonationCreate
):
    """
    Create a new donation.
    """
    donation = Donation(
        **donation_in.model_dump(exclude_unset=True),
        user_id=current_user.id
    )
    
    session.add(donation)
    session.commit()
    session.refresh(donation)
    
    response = DonationPublic.model_validate(donation.model_dump())
    return response


@router.delete("/{donation_id}", dependencies=[Depends(get_current_superuser)], tags=['superuser'])
async def delete_donation(
    session: SessionDep,
    donation_id: uuid.UUID
):
    """
    Delete a donation.
    """
    donation = session.get(Donation, donation_id)
    if not donation:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Donation not found")
    
    session.delete(donation)
    session.commit()
    
    return JSONResponse(status_code=status.HTTP_204_NO_CONTENT, content={"message": "Donation deleted successfully"})
