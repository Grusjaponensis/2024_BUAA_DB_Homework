import uuid, datetime
from enum import Enum

from sqlmodel import Field, SQLModel, Relationship
from pydantic import BaseModel

UTC_8 = datetime.timezone(datetime.timedelta(hours=8))


class ActivityType(str, Enum):
    rescue = "rescue"

# - MARK: ActivityBase
class ActivityBase(SQLModel):
	"""
	Base model for all Activity
	- id: `uuid.UUID`
	- title: `str`
	- description: `str`
	- location: `str`
	- starts_at: `datetime.datetime`
	- ends_at: `datetime.datetime`
	- signup_start_at: `datetime.datetime | None`
	- signup_ends_at: `datetime.datetime | None`
	- created_at: `datetime.datetime`
	"""
	id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
	type: ActivityType = Field(...)
	title: str = Field(max_length=100)
	description: str = Field(max_length=1024)
	location: str = Field(max_length=100)
	starts_at: datetime.datetime = Field(...)
	ends_at: datetime.datetime = Field(...)
	signup_starts_at: datetime.datetime | None = Field(default=None)
	signup_ends_at: datetime.datetime | None = Field(default=None)
	created_at: datetime.datetime = Field(default_factory=lambda: datetime.datetime.now(UTC_8))
    

# - MARK: ActivityCreate
class ActivityCreate(BaseModel):
    type: ActivityType
    title: str
    description: str
    location: str
    starts_at: datetime.datetime
    ends_at: datetime.datetime
    signup_starts_at: datetime.datetime | None = None
    signup_ends_at: datetime.datetime | None = None
    max_participants: int # a range of [0 - max_participants]
    

# - MARK: ActivityUpdate
class ActivityUpdate(BaseModel):
    type: ActivityType | None = Field(default=None)
    title: str | None = Field(default=None, max_length=128)
    description: str | None = Field(default=None, max_length=1024)
    location: str | None = Field(default=None, max_length=128)
    starts_at: datetime.datetime | None = Field(default=None)
    ends_at: datetime.datetime | None = Field(default=None)
    signup_starts_at: datetime.datetime | None = Field(default=None)
    signup_ends_at: datetime.datetime | None = Field(default=None)
    max_participants: int | None = Field(default=None, ge=0)


# - MARK: ActivityPublic
class ActivityPublic(BaseModel):
    id: uuid.UUID
    type: ActivityType
    title: str
    description: str
    location: str
    starts_at: datetime.datetime
    ends_at: datetime.datetime
    signup_starts_at: datetime.datetime | None = None
    signup_ends_at: datetime.datetime | None = None
    max_participants: int
    current_participants: int
    creator_id: uuid.UUID
    created_at: datetime.datetime
