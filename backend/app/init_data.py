from sqlmodel import Session

from app.core.db import engine, init_db


def init() -> None:
    with Session(engine) as session:
        init_db(session)
