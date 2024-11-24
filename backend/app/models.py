import uuid, random, string

from fastapi import Form
from pydantic import EmailStr
from sqlmodel import SQLModel, Field

from app.core.config import settings


USER_EMAIL_MAX_LENGTH = 100
USER_PASSWORD_MIN_LENGTH = 8
USER_PASSWORD_MAX_LENGTH = 100
USER_NICKNAME_MAX_LENGTH = 50


# - MARK: User models
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
    # other properties

    
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
    email: EmailStr = Field(default=Form(...), max_length=USER_EMAIL_MAX_LENGTH)
    password: str = Field(default=Form(...), min_length=USER_PASSWORD_MIN_LENGTH, max_length=USER_PASSWORD_MAX_LENGTH)
    nickname: str | None = Field(default=Form(None), max_length=USER_NICKNAME_MAX_LENGTH)

    
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
    

# - MARK: Token models
class Token(SQLModel):
    access_token: str
    token_type: str = "bearer"
    
    
class TokenPayload(SQLModel):
    sub: str | None = None
    

# - MARK: Message models
class Message(SQLModel):
    """Model to return a single message for display"""
    message: str
    

