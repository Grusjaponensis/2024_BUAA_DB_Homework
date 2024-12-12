import uuid, datetime

from pydantic import BaseModel
from sqlmodel import SQLModel, Field

from app.models.user import User
from app.core.config import settings


class Donation(SQLModel, table=True):
    """
    Base model for donation.
    
    Attributes:
     - id: uuid.UUID
     - user_id: uuid.UUID
     - amount: float
     - message: str | None
     - donated_at: datetime.datetime = datetime.datetime.now(settings.UTC_8)
     - is_anonymous: bool = False
    """
    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    user_id: uuid.UUID = Field(foreign_key="user.id", index=True, ondelete="CASCADE")
    amount: float = Field(ge=0, index=True)
    message: str | None = Field(default=None, max_length=255)
    donated_at: datetime.datetime = Field(default_factory=lambda: datetime.datetime.now(settings.UTC_8), index=True)
    is_anonymous: bool = Field(default=False)
    

class DonationCreate(BaseModel):
    """
    Model for creating donation
    
    Attributes:
     - amount: float
     - message: str | None = None
     - is_anonymous: bool = False
    """
    amount: float
    message: str | None = None
    donated_at: datetime.datetime = datetime.datetime.now(settings.UTC_8)
    is_anonymous: bool = False
    
    
class DonationPublic(BaseModel):
    """
    Model for donation public info
    
    Attributes:
     - id: uuid.UUID
     - user_id: uuid.UUID
     - amount: float
     - message: str | None
     - donated_at: datetime.datetime
     - is_anonymous: bool
    """
    id: uuid.UUID
    user_id: uuid.UUID
    amount: float
    message: str | None = None
    donated_at: datetime.datetime
    is_anonymous: bool