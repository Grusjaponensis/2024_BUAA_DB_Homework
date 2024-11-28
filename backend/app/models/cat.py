import uuid, datetime
from enum import Enum

from sqlmodel import Field, SQLModel

UTC_8 = datetime.timezone(datetime.timedelta(hours=8))


class HealthCondition(int, Enum):
    HEALTHY = 1
    SICK = 2
    VACCINATED = 3
    DEAD = 4


class CatBase(SQLModel):
    name: str = Field(index=True, max_length=256)
    is_male: bool = Field(default=True)
    age: int | None = Field(default=None, ge=0, le=30)
    # latest_location_id: uuid.UUID | None = Field(default=None, foreign_key="location.id", index=True)
    health_condition: int = Field(default=1, ge=1, le=4)
    description: str | None = Field(default=None, max_length=1024)
    created_at: datetime.datetime = Field(default_factory=lambda: datetime.datetime.now(tz=UTC_8))
    

class Cat(CatBase, table=True):
    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)