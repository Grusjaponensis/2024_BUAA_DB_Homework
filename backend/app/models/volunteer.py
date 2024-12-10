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
