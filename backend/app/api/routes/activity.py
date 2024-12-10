import uuid, logging

from fastapi import (
    APIRouter, HTTPException, Depends, Form
)
from fastapi.responses import JSONResponse
from sqlmodel import select, func

import app.crud as crud
from app.api.deps import (
    LoginRequired,
    CurrentUser,
    SessionDep,
    get_current_superuser
)
from app.models.user import Activity
from app.models.activity import (
    ActivityCreate,
    ActivityPublic,
    ActivityUpdate
)
from app.core.config import settings


logger = logging.getLogger(__name__)


router = APIRouter()


# - MARK: get all activities
@router.get("/", response_model=list[ActivityPublic], dependencies=[LoginRequired])
async def get_activities(
    session: SessionDep, offset: int = 0, limit: int = 100
):
    """
    Get all activities.
    """
    activities = session.exec(select(Activity).offset(offset).limit(limit))
    response = [ActivityPublic.model_validate(activity.model_dump()) for activity in activities]
    return response


# - MARK: get activity by id
@router.get("/{activity_id}", response_model=ActivityPublic, dependencies=[LoginRequired])
async def get_activity_by_id(session: SessionDep, activity_id: uuid.UUID):
    """
    Get an activity by id.
    """
    activity = session.get(Activity, activity_id)
    if not activity:
        raise HTTPException(status_code=404, detail="Activity not found")
    return ActivityPublic.model_validate(activity.model_dump())


# - MARK: create activity
@router.post("/", response_model=ActivityPublic)
async def create_activity(
    session: SessionDep, 
    current_user: CurrentUser, 
    activity_in: ActivityCreate 
):
    """
    Create a new activity.
    """
    # TODO: whether to check if a user is superuser or volunteer
    activity = Activity(
        **activity_in.model_dump(),
        creator_id=current_user.id
    )
    session.add(activity)
    session.commit()
    session.refresh(activity)
    
    return ActivityPublic(**activity.model_dump())


# - MARK: update activity
@router.patch("/{activity_id}", response_model=ActivityPublic)
async def update_activity(
    session: SessionDep, current_user: CurrentUser, activity_id: uuid.UUID, activity_in: ActivityUpdate
):
    """
    Update an activity.
    """
    activity = session.get(Activity, activity_id)
    if not activity:
        raise HTTPException(status_code=404, detail="Activity not found")
    if activity.creator_id != current_user.id: # is this necessary?
        raise HTTPException(status_code=403, detail="Not authorized to perform this action")
    
    activity.sqlmodel_update(activity_in.model_dump(exclude_unset=True))
    session.add(activity)
    session.commit()
    session.refresh(activity)
    return ActivityPublic.model_validate(activity.model_dump())


# - MARK: delete activity
@router.delete("/{activity_id}", dependencies=[LoginRequired])
async def delete_activity(
    session: SessionDep, current_user: CurrentUser, activity_id: uuid.UUID
):
    """
    Delete an activity.
    """
    activity = session.get(Activity, activity_id)
    if not activity:
        raise HTTPException(status_code=404, detail="Activity not found")
    if activity.creator_id != current_user.id:
        raise HTTPException(status_code=403, detail="Not authorized to perform this action")
    
    session.delete(activity)
    session.commit()
    return JSONResponse(status_code=200, content={"message": "Activity deleted successfully"})
