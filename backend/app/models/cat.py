import uuid, datetime
from enum import Enum

from sqlmodel import Field, SQLModel, Relationship
from pydantic import BaseModel

from app.models.user import User

UTC_8 = datetime.timezone(datetime.timedelta(hours=8))


# - MARK: HealthEnum
class HealthCondition(int, Enum):
    """
    Enum for health conditions of a cat:
    - HEALTHY: 1
    - SICK: 2
    - VACCINATED: 3
    - DEAD: 4
    """
    HEALTHY = 1
    SICK = 2
    VACCINATED = 3
    DEAD = 4


# - MARK: CatBase
class CatBase(SQLModel):
    """
    Base model for Cat:
    - name: Cat's name (string, indexed, max length 256)
    - is_male: Gender of the cat (boolean, default=True)
    - age: Cat's age (int, optional, 0-30)
    - health_condition: Cat's health status (int, 1-4, default=1)
    - description: Description of the cat (string, optional, max length 1024)
    - created_at: Timestamp when the cat was added (datetime, default=current time)
    """
    name: str = Field(index=True, max_length=256)
    is_male: bool = Field(default=True)
    age: int | None = Field(default=None, ge=0, le=30)
    health_condition: int = Field(default=1, ge=1, le=4)
    description: str | None = Field(default=None, max_length=1024)
    created_at: datetime.datetime = Field(default_factory=lambda: datetime.datetime.now(tz=UTC_8))
        

# - MARK: Cat Model
class Cat(CatBase, table=True):
    """
    - id: Primary key (UUID, auto-generated)
    - name: Cat's name (string, indexed, max length 256)
    - is_male: Gender of the cat (boolean, default=True)
    - age: Cat's age (int, optional, 0-30)
    - health_condition: Cat's health status (int, 1-4, default=1)
    - description: Description of the cat (string, optional, max length 1024)
    - created_at: Timestamp when the cat was added (datetime, default=current time)
    """
    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    
    # relationships
    images: list["CatMedia"] = Relationship(back_populates="cat_ref", cascade_delete=True)
    locations: list["CatLocation"] = Relationship(back_populates="cat_ref", cascade_delete=True)
        

class CatMedia(SQLModel, table=True):
    """
    CatMedia model representing the table:
    - id: Primary key (UUID, auto-generated)
    - cat_id: Foreign key to Cat (UUID)
    - image_url: URL of the image
    """
    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    cat_id: uuid.UUID = Field(foreign_key="cat.id", index=True, ondelete="CASCADE")
    image_url: str

    # relationships
    cat_ref: Cat = Relationship(back_populates="images")

# - MARK: CatLocation
class CatLocation(SQLModel, table=True):
    """
    CatLocation model representing the table:
    - id: Primary key (UUID, auto-generated)
    - cat_id: Foreign key to Cat (UUID)
    - user_id: Foreign key to User (UUID)
    - longitude: Longitude of the location (-180 to 180)
    - latitude: Latitude of the location (-90 to 90)
    - created_at: Timestamp when the location was recorded (datetime, default=current time)
    """
    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    cat_id: uuid.UUID = Field(foreign_key="cat.id", index=True, ondelete="CASCADE")
    user_id: uuid.UUID = Field(foreign_key="user.id", index=True)
    longitude: float = Field(ge=-180, le=180)
    latitude: float = Field(ge=-90, le=90)
    created_at: datetime.datetime = Field(default_factory=lambda: datetime.datetime.now(tz=UTC_8))
    
    # relationships
    cat_ref: Cat = Relationship(back_populates="locations")
        

# - MARK: CatCreate
class CatCreate(CatBase):
    """
    Data model for creating a new cat:
    - Inherits attributes from CatBase.
    - Allows optional overrides for is_male, age, health_condition, and description.
    """
    is_male: bool | None = Field(default=True)
    age: int | None = Field(default=None, ge=0, le=30)
    health_condition: int | None = Field(default=1, ge=1, le=4)
    description: str | None = Field(default=None, max_length=1024)


# - MARK: CatLocCreate
class CatLocationCreate(BaseModel):
    longitude: float = Field(ge=-180, le=180)
    latitude: float = Field(ge=-90, le=90)


# - MARK: API Models
class CatUpdateInfo(BaseModel):
    """
    Data model for updating a cat's information:
    - name: New name (string, optional, max length 256)
    - is_male: New gender (boolean, optional)
    - age: New age (int, optional, 0-30)
    - health_condition: New health status (int, optional, 1-4)
    - description: New description (string, optional, max length 1024)
    """
    name: str | None = Field(default=None, max_length=256)
    is_male: bool | None = Field(default=None)
    age: int | None = Field(default=None, ge=0, le=30)
    health_condition: int | None = Field(default=None, ge=1, le=4)
    description: str | None = Field(default=None, max_length=1024)
    

class CatUpdateLocation(BaseModel):
    """
    Data model for updating a cat's location:
    - longitude: New longitude (-180 to 180, optional)
    - latitude: New latitude (-90 to 90, optional)
    """
    longitude: float | None = Field(default=None, ge=-180, le=180)
    latitude: float | None = Field(default=None, ge=-90, le=90)


class CatPublic(BaseModel):
    """
    Public representation of a cat:
    - id: Cat's ID (UUID)
    - name: Cat's name (string)
    - is_male: Gender of the cat (boolean, default=True)
    - age: Cat's age (int, optional)
    - latest_longitude: Latest recorded longitude (float, optional)
    - latest_latitude: Latest recorded latitude (float, optional)
    - health_condition: Health status (int)
    - description: Cat's description (string, optional)
    """
    id: uuid.UUID
    name: str
    is_male: bool = True
    age: int | None = None
    latest_longitude: float | None = None
    latest_latitude: float | None = None
    health_condition: int
    description: str | None = None
    created_at: datetime.datetime


class CatsPublic(BaseModel):
    """
    List of public representations of cats:
    - cats: List of CatPublic instances
    """
    cats: list[CatPublic]


class CatLocationPublic(BaseModel):
    """
    Public representation of a cat's location:
    - id: Location ID (UUID)
    - user_id: User's ID (UUID)
    - longitude: Longitude of the location (-180 to 180)
    - latitude: Latitude of the location (-90 to 90)
    - created_at: Timestamp when the location was recorded (datetime)
    """
    id: uuid.UUID
    user_id: uuid.UUID
    longitude: float
    latitude: float
    created_at: datetime.datetime