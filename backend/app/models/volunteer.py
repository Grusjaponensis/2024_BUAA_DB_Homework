import uuid, datetime, logging

from pydantic import BaseModel, Field

from app.models.user import ApplicationStatus


logger = logging.getLogger(__name__)


UTC_8 = datetime.timezone(datetime.timedelta(hours=8))
    

class ActivityRegistrationUpdate(BaseModel):
    """
    Data model for updating the status of an existing volunteer application.
    Attributes:
    - status: New status of the application (Approved, Rejected, Pending)
    - updated_at: The date and time when the application status was updated
    """
    status: ApplicationStatus


class VolunteerApplicationCreate(BaseModel):
    """
    Model to create a volunteer application.
    Attributes:
    - user_id: The ID of the user who is applying for volunteering
    - reason: The reason for applying for volunteering
    """
    reason: str = Field(max_length=1024)


class VolunteerApplicationUpdate(BaseModel):
    """
    Model to update a volunteer application status (perform by superuser).
    Attributes:
    - status: The new status of the volunteer application
    """
    status: ApplicationStatus
