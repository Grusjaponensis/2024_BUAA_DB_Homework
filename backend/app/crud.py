import logging, uuid
from typing import Any

from fastapi import HTTPException
from sqlmodel import Session, select, func

from app.core.security import get_password_hash, verify_password

from app.models.user import User, UserCreate, UserUpdate
from app.models.post import Post, Like, PostTag
from app.models.cat import Cat, CatLocation


logger = logging.getLogger(__name__)


# - MARK: User CRUD
def create_user(*, session: Session, user_create: UserCreate) -> User:
    user_to_store = User.model_validate(
        user_create, update={"hashed_password": get_password_hash(user_create.password)}
    )
    session.add(user_to_store)
    session.commit()
    session.refresh(user_to_store)
    return user_to_store

def update_user(*, session: Session, db_user: User, user_in: UserUpdate) -> Any:
    user_data = user_in.model_dump(exclude_unset=True)
    extra_data = {}
    
    if "password" in user_data:
        # update password hash if password is provided
        hashed_password = get_password_hash(user_data['password'])
        extra_data['hashed_password'] = hashed_password
    
    db_user.sqlmodel_update(user_data, update=extra_data)
    session.add(db_user)
    session.commit()
    session.refresh(db_user)
    return db_user

def get_user_by_email(*, session: Session, email: str) -> User | None:
    """
    find the user by email in database, return `None` if not found
    """
    select_statement = select(User).where(User.email == email)
    session_user = session.exec(select_statement).first()
    return session_user

def authenticate(*, session: Session, email: str, password: str) -> User | None:
    db_user = get_user_by_email(session=session, email=email)
    if not db_user:
        return None
    if not verify_password(password, db_user.hashed_password):
        return None
    return db_user


# - MARK: Post CRUD
def get_post_likes_count(*, session: Session, post_id: uuid.UUID) -> int:
    """
    Get the number of likes for a post
    """
    if not post_id:
        return 0
    if session.exec(select(Post).where(Post.id == post_id)).first() is None:
        raise HTTPException(status_code=404, detail="Post not found")
    return session.exec(select(func.count(Like.post_id)).where(Like.post_id == post_id)).one()


def get_all_tags(*, session: Session) -> list[str]:
    """
    Get all tags in the database
    """
    tags = session.exec(select(PostTag)).all()
    return [tag.name for tag in tags]


def get_like_status(*, session: Session, user_id: uuid.UUID, post_id: uuid.UUID) -> bool:
    """
    Check if a user has liked a post
    """
    if not user_id or not post_id:
        return False
    like = session.get(Like, (user_id, post_id))
    return like is not None


# - MARK: Cat CRUD
def get_latest_cat_location(session: Session, cat_id: uuid.UUID):
    """
    Get the latest cat location of a specific cat
    """
    if not cat_id:
        return None

    cat_location = session.exec(
        select(CatLocation).where(CatLocation.cat_id == cat_id).order_by(CatLocation.created_at.desc())
    ).first()
    return cat_location