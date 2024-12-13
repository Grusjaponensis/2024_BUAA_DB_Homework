import uuid, logging
from datetime import datetime, timedelta
from typing import Any

import numpy as np
import pandas as pd

from fastapi import (
    APIRouter, Depends, HTTPException, status, Query
)
from fastapi.responses import JSONResponse, FileResponse
from sqlmodel import func, select

from app.api.deps import (
    CurrentUser,
    LoginRequired,
    SessionDep,
    get_current_superuser
)
from app.models.donation import Donation, DonationCreate, DonationPublic
from app.core.config import settings


logger = logging.getLogger(__name__)


router = APIRouter()


@router.get("/export", tags=['superuser'], dependencies=[Depends(get_current_superuser)])
async def export_donations(
    session: SessionDep,
    start_date: str = Query(None, description="Start date in format YYYY-MM-DD"),
    end_date: str = Query(None, description="End date in format YYYY-MM-DD")
):
    """
    Export donations to excel file.
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
        start = end - timedelta(days=365) # default for one year, well I know the time range selection will not be completed
    
    donations = session.exec(
        select(func.date(Donation.donated_at), func.sum(Donation.amount), func.count(Donation.id))
            .where(Donation.donated_at >= start)
            .where(Donation.donated_at <= end)
            .group_by(func.date(Donation.donated_at))
            .order_by(func.date(Donation.donated_at))
    ).all()

    aggregated_data: list[dict[str, Any]] = [
        {"date": donation[0], "amount": donation[1] or 0, "count": donation[2] or 0}
        for donation in donations
    ]

    df = pd.DataFrame(aggregated_data)
    df.set_index("date", inplace=True)
    df.fillna(0, inplace=True)

    file_path = f"donations_{start.strftime('%Y-%m-%d')}_{end.strftime('%Y-%m-%d')}.xlsx"
    try:
        with pd.ExcelWriter(file_path, engine="openpyxl") as writer:
            df.to_excel(writer, sheet_name="Donations")
    except Exception as e:
        logger.error(f"Failed to write Excel file: {e}")
        raise HTTPException(status_code=500, detail="Failed to generate Excel file.")
    
    response = FileResponse(file_path, media_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")
    response.headers["Content-Disposition"] = f"attachment; filename=donations_{start.strftime('%Y-%m-%d')}_{end.strftime('%Y-%m-%d')}.xlsx"

    return response


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
