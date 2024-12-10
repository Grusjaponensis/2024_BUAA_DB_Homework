import uuid, logging, datetime

from fastapi import (
    APIRouter, HTTPException, Depends
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
from app.models.user import (
    ActivityRegistration, User, Activity,
    VolunteerApplication
)
from app.models.volunteer import ActivityRegistrationUpdate
from app.core.config import settings


logger = logging.getLogger(__name__)


router = APIRouter()

# - MARK: sudo all registrations
@router.get("/", response_model=list[ActivityRegistration], dependencies=[Depends(get_current_superuser)], tags=["superuser"])
async def get_all_activity_registrations(session: SessionDep):
    """
    Get all activity registrations by superuser
    """
    all_registrations = session.exec(select(ActivityRegistration)).all()
    return [ActivityRegistration(**registration.model_dump()) for registration in all_registrations]


# - MARK: my registrations
@router.get("/my", response_model=list[ActivityRegistration])
async def get_activity_registrations_for_volunteer(
    session: SessionDep,
    current_user: CurrentUser
):
    """
    Get all volunteer applications for the current user
    """
    if not current_user.is_volunteer and not current_user.is_superuser:
        raise HTTPException(status_code=403, detail="你还不是志愿者，请先申请成为志愿者吧")
            
    applications = session.exec(
        select(ActivityRegistration).where(ActivityRegistration.user_id == current_user.id)
    )
    return [ActivityRegistration(**application.model_dump()) for application in applications]


@router.get("/applications", response_model=list[VolunteerApplication])
async def get_volunteer_applications(
    session: SessionDep,
    current_user: CurrentUser
):
    """
    Get all records of trying to apply to be a volunteer.
    If CurrentUser is superuser, return all applications.
    Else only return the current user's applications.
    """
    if current_user.is_superuser:
        applications = session.exec(select(VolunteerApplication))
        return [VolunteerApplication(**application.model_dump()) for application in applications]
    
    applications = session.exec(select(VolunteerApplication).where(VolunteerApplication.user_id == current_user.id))
    return [VolunteerApplication(**application.model_dump()) for application in applications]

# - MARK: get registration by id
@router.get("/{activity_id}", response_model=ActivityRegistration)
async def get_activity_registration_by_id(
    session: SessionDep, current_user: CurrentUser, activity_id: uuid.UUID
):
    """
    Get a activity registration by id
    """
    if not current_user.is_volunteer and not current_user.is_superuser:
        raise HTTPException(status_code=403, detail="你还不是志愿者，请先申请成为志愿者吧")
    
    application = session.get(ActivityRegistration, (current_user.id, activity_id))
    if not application:
        raise HTTPException(status_code=404, detail="Application not found")
    return application


# - MARK: create registration
@router.post("/{activity_id}", response_model=ActivityRegistration)
async def create_activity_registration(
    session: SessionDep,
    current_user: CurrentUser,
    activity_id: uuid.UUID
):
    """
    Create a new volunteer registration for an activity
    """
    if not current_user.is_volunteer and not current_user.is_superuser:
        raise HTTPException(status_code=403, detail="你还不是志愿者，请先申请成为志愿者吧")        
    
    exist_application = session.get(ActivityRegistration, (current_user.id, activity_id))
    if exist_application:
        raise HTTPException(status_code=400, detail="You have already applied for this activity")
    
    new_registration = ActivityRegistration(
        user_id=current_user.id, 
        activity_id=activity_id,
    )
    session.add(new_registration)
    session.commit()
    session.refresh(new_registration)
    return new_registration
    
    
# - MARK: update registration
@router.patch("/{activity_id}", response_model=ActivityRegistration, dependencies=[Depends(get_current_superuser)], tags=["superuser"])
async def update_activity_registration(
    session: SessionDep,
    applicant_id: uuid.UUID, # user_id
    activity_id: uuid.UUID,
    volunteer_application_in: ActivityRegistrationUpdate
):
    """
    **approve** or **reject** a volunteer's activity registration
    """
    user = session.get(User, applicant_id)
    activity = session.get(Activity, activity_id)
    registration = session.get(ActivityRegistration, (applicant_id, activity_id))
    if not registration or not user or not activity:
        raise HTTPException(status_code=404, detail="Registration or user or activity not found")
    
    registration.sqlmodel_update(volunteer_application_in.model_dump(exclude_unset=True))
    registration.updated_at = datetime.datetime.now(settings.UTC_8)
    
    # NOTE: partially relation could not use relationship! 
    # (e.g. ActivityRegistration has an attribute of status, which could not insert into user.activity directly)
    session.add(registration)
    session.commit()
    session.refresh(registration)
    return registration