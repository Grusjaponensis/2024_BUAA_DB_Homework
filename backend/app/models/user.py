import uuid, random, string, datetime
from enum import Enum

from pydantic import EmailStr, BaseModel
from sqlmodel import SQLModel, Field, Relationship

from app.models.activity import ActivityBase
from app.core.config import settings


USER_EMAIL_MAX_LENGTH = 100
USER_PASSWORD_MIN_LENGTH = 8
USER_PASSWORD_MAX_LENGTH = 100
USER_NICKNAME_MAX_LENGTH = 50


UTC_8 = datetime.timezone(datetime.timedelta(hours=8))


# - MARK: Activity registration
class ApplicationStatus(str, Enum):
    """
    Enum to represent the status of a volunteer application.
    Possible values:
    - PENDING: Application is pending review
    - APPROVED: Application is approved
    - REJECTED: Application is rejected
    """
    PENDING = "pending"
    APPROVED = "approved"
    REJECTED = "rejected"


class ActivityRegistration(SQLModel, table=True):
    """
    Represents a volunteer application for an activity.
    Attributes:
    - user_id: Foreign key referencing the user applying
    - activity_id: Foreign key referencing the activity
    - reason: Reason for applying to the activity
    - status: Status of the application (Pending, Approved, Rejected)
    - created_at: Date and time when the application was created
    - updated_at: Date and time when the application was last updated
    """
    user_id: uuid.UUID = Field(foreign_key="user.id", primary_key=True, index=True)
    activity_id: uuid.UUID = Field(foreign_key="activity.id", primary_key=True, index=True)
    status: ApplicationStatus = Field(default=ApplicationStatus.PENDING)
    created_at: datetime.datetime = Field(default_factory=lambda: datetime.datetime.now(UTC_8))
    updated_at: datetime.datetime = Field(default_factory=lambda: datetime.datetime.now(UTC_8))


# - MARK: Activity
class Activity(ActivityBase, table=True):
    """
    Represents an activity that volunteers can apply for.
    Attributes:
    - creator_id: ID of the user who created the activity
    - max_participants: Maximum number of participants allowed
    - signup_start_at: Start date and time for accepting participants
    - signup_end_at: End date and time for accepting participants
    - participants: List of users who have applied for the activity, linked with VolunteerApplication
    """
    creator_id: uuid.UUID = Field(foreign_key="user.id")
    max_participants: int


# - MARK: Volunteer application
class VolunteerApplication(SQLModel, table=True):
    """
    Represents user trying to apply to be a volunteer.
    Attributes:
    - user_id: Foreign key referencing the user applying
    - reason: Reason for applying to the activity
    - status: Status of the application (Pending, Approved, Rejected)
    - created_at: Date and time when the application was created
    - updated_at: Date and time when the application was last updated
    """
    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    user_id: uuid.UUID = Field(foreign_key="user.id", index=True)
    status: ApplicationStatus = Field(default=ApplicationStatus.PENDING)
    created_at: datetime.datetime = Field(default_factory=lambda: datetime.datetime.now(UTC_8))
    updated_at: datetime.datetime = Field(default_factory=lambda: datetime.datetime.now(UTC_8))


# User model for database
class UserBase(SQLModel):
    """
    Shared properties
    ```
    email: EmailStr = Field(max_length=100)
    nickname: str | None
    is_superuser: bool = False
    is_volunteer: bool = False  
    avatar_url: str = DEFAULT
    ```
    """
    email: EmailStr = Field(unique=True, index=True, max_length=USER_EMAIL_MAX_LENGTH)
    nickname: str | None = Field(
        default="User_" + "".join(random.sample(string.ascii_letters + string.digits, 12)), 
        max_length=USER_NICKNAME_MAX_LENGTH
    )
    is_superuser: bool = False
    is_volunteer: bool = False
    avatar_url: str = Field(default=settings.DEFAULT_USER_AVATAR_URL)


# Properties to receive via API on creation
class UserCreate(UserBase):
    """
    Properties to receive via API on creation.
    ```
    # from UserBase model
    email: EmailStr = Field(max_length=100)
    nickname: str | None
    is_superuser: bool = False
    is_volunteer: bool = False
    avatar_url: str = DEFAULT
    
    password: str
    ```
    """
    password: str = Field(min_length=USER_PASSWORD_MIN_LENGTH, max_length=USER_PASSWORD_MAX_LENGTH)
    
    
# Properties to receive via API on update, all are **optional**
class UserUpdate(UserBase):
    """
    Properties to receive via API on update, all are **optional**. 
    
    **Note:** Used for superuser update.
    ```
    email: EmailStr | None # And other fields from UserBase model
    password: str | None
    ```
    """
    email: EmailStr | None = Field(default=None, max_length=USER_EMAIL_MAX_LENGTH)
    password: str | None = Field(default=None, min_length=USER_PASSWORD_MIN_LENGTH, max_length=USER_PASSWORD_MAX_LENGTH)


# - MARK: User
# Database model, database table inferred from class name
class User(UserBase, table=True):
    """
    Database model, database table inferred from class name.
    ```
    # include all fields from UserBase model
    id: uuid.UUID
    hashed_password: str
    ```
    """    
    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    hashed_password: str 

    
# Properties to return via API, id is always required
class UserPublic(UserBase):
    id: uuid.UUID
    
    
class UserRegister(SQLModel):
    """
    Fields:
    ```
    email: str
    password: str
    nickname: str | None = None
    avatar_url: str = DEFAULT
    ```
    """
    email: EmailStr = Field(max_length=USER_EMAIL_MAX_LENGTH)
    password: str = Field(min_length=USER_PASSWORD_MIN_LENGTH, max_length=USER_PASSWORD_MAX_LENGTH)
    nickname: str | None = Field(default=None, max_length=USER_NICKNAME_MAX_LENGTH)

    
class UserUpdateProfile(SQLModel):
    """
    Fields:
    ```
    email: str | None
    nickname: str | None
    new_avatar_url: str = DEFAULT
    ```
    """
    email: EmailStr | None = Field(default=None, max_length=USER_EMAIL_MAX_LENGTH)
    nickname: str | None = Field(default=None, max_length=USER_NICKNAME_MAX_LENGTH)


class UserUpdatePassword(SQLModel):
    """
    Model to update password.
    ```
    old_password: str
    new_password: str
    ```
    """
    old_password: str = Field(min_length=USER_PASSWORD_MIN_LENGTH, max_length=USER_PASSWORD_MAX_LENGTH)
    new_password: str = Field(min_length=USER_PASSWORD_MIN_LENGTH, max_length=USER_PASSWORD_MAX_LENGTH)
    

class UserUpdateAvatar(SQLModel):
    """
    Model to update avatar.
    ```
    new_avatar_url: str
    ```
    """
    new_avatar_url: str = Field(default=settings.DEFAULT_USER_AVATAR_URL)


class UsersPublic(SQLModel):
    data: list[UserPublic]
    count: int
    

# - MARK: Message models
class Message(SQLModel):
    """Model to return a single message for display"""
    message: str


# - MARK: Token models
class Token(SQLModel):
    access_token: str
    token_type: str = "bearer"
    
    
class TokenPayload(SQLModel):
    sub: str | None = None
