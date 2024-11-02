import logging

from sqlmodel import Session, create_engine, select

from app.core.config import settings
from app.models import User, UserCreate
import app.crud as crud

engine = create_engine(settings.MYSQL_DATABASE_URI)

def init_db(session: Session) -> None:
    from sqlmodel import SQLModel
    # Create all tables
    SQLModel.metadata.create_all(engine)

    superuser = session.exec(
        select(User).where(User.email == settings.FIRST_SUPERUSER)
    ).first()
    if not superuser:
        superuser_in = UserCreate(
            email=settings.FIRST_SUPERUSER,
            password=settings.FIRST_SUPERUSER_PASSWORD,
            is_superuser=True,
        )
        superuser = crud.create_user(session=session, user_create=superuser_in)
        logging.info(f"Create superuser: {superuser.email}")
        