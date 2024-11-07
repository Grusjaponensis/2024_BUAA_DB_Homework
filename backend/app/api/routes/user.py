from typing import Any
import uuid

from fastapi import (
    APIRouter, Depends, HTTPException, status, 
)
from sqlmodel import func, select

import app.crud as crud
from app.api.deps import (
    CurrentUser,
    SessionDep,
    get_current_superuser
)
from app.models import (
    User, UserCreate, UserPublic, 
    UserUpdate, UsersPublic, UserUpdateProfile,
    UpdatePassword, Message, UserRegister
)
from app.core.security import get_password_hash, verify_password, create_access_token


router = APIRouter()


# - MARK: get user profile -
@router.get("/profile", response_model=UserPublic)
async def read_user_profile(current_user: CurrentUser) -> Any:
    """
    Get current user profile.
    """
    return current_user


# - MARK: update user profile -
@router.patch("/profile", response_model=UserPublic)
async def update_user_profile(
    *, session: SessionDep, user_in: UserUpdateProfile, current_user: CurrentUser
) -> Any:
    """
    Update user profile.
    """
    if user_in.email:
        existing_user = crud.get_user_by_email(session=session, email=user_in.email)
        if existing_user and existing_user.id != current_user.id:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="Email already registered",
            )
    user_data = user_in.model_dump(exclude_unset=True)
    current_user.sqlmodel_update(user_data)
    session.add(current_user)
    session.commit()
    session.refresh(current_user)
    return current_user


# - MARK: update user password -
@router.patch("/profile/password", response_model=Message)
async def update_user_password(
    *, session: SessionDep, current_user: CurrentUser, body: UpdatePassword
) -> Any:
    """
    Update user password.
    """
    if not verify_password(body.old_password, current_user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Incorrect password",
        )
    if body.new_password == body.old_password:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="New password cannot be the same as the old one",
        )
    hashed_password = get_password_hash(body.new_password)
    current_user.hashed_password = hashed_password
    session.add(current_user)
    session.commit()
    return Message(message="Password updated successfully")


# TODO: Implement user deletion


# - MARK: user registration -
@router.post("/register")
async def register_user(*, session: SessionDep, user_in: UserRegister) -> Any:
    """
    Register a new user and then log in.
    """
    existing_user = crud.get_user_by_email(session=session, email=user_in.email)
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Email already registered",
        )
    user_to_create = UserCreate.model_validate(user_in)
    user = crud.create_user(session=session, user_create=user_to_create)
    access_token = create_access_token(subject={"sub": user.email})
    # do not need to login again
    return {"access_token": access_token, "token_type": "bearer"}


# - MARK: superuser routes -
@router.get(
    "/", dependencies=[Depends(get_current_superuser)], response_model=UsersPublic
)
async def read_users_by_superuser(session: SessionDep, skip: int = 0, limit: int = 100) -> Any:
    """
    Retrieve users.
    """
    count_stmt = select(func.count()).select_from(User)
    count = session.exec(count_stmt).one()
    
    retrieve_stmt = select(User).offset(skip).limit(limit)
    users = session.exec(retrieve_stmt).all()
    
    return UsersPublic(data=users, count=count)


@router.post(
    "/", dependencies=[Depends(get_current_superuser)], response_model=UserPublic
)
async def create_user_by_superuser(*, session: SessionDep, user_in: UserCreate) -> Any:
    """
    Create a new user.
    """
    user = crud.get_user_by_email(session=session, email=user_in.email)
    if user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already registered",
        )
    user = crud.create_user(session=session, user_create=user_in)
    # Optional: send email confirmation
    
    return user


@router.patch(
    "/{user_id}", dependencies=[Depends(get_current_superuser)], response_model=UserPublic
)
async def update_user_by_superuser(
    *, session: SessionDep, user_id: uuid.UUID, user_in: UserUpdate
) -> Any:
    """
    Update a user, only performable by a superuser.
    """
    db_user = session.get(User, user_id)
    if not db_user:
        raise HTTPException(status_code=404, detail=f"User of id {user_id} not found")

    is_superuser = db_user.is_superuser
    
    if user_in.email:
        existing_user = crud.get_user_by_email(session=session, email=user_in.email)
        # Check if email already registered and not the same user
        if existing_user and existing_user.id != user_id:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="Email already registered",
            )
    user_data = user_in.model_dump(exclude_unset=True)
    db_user.sqlmodel_update(user_data)
    session.add(db_user)
    session.commit()
    session.refresh(db_user)
    return db_user


@router.delete("/{user_id}", dependencies=[Depends(get_current_superuser)])
def delete_user_by_superuser(
    session: SessionDep, current_user: CurrentUser, user_id: uuid.UUID
) -> Message:
    """
    Delete a user.
    """
    user = session.get(User, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    if user == current_user:
        raise HTTPException(
            status_code=403, detail="Super users are not allowed to delete themselves"
        )
    session.delete(user)
    session.commit()
    return Message(message="User deleted successfully")


@router.get("/{user_id}", response_model=UserPublic)
def read_user_by_id(
    user_id: uuid.UUID, session: SessionDep, current_user: CurrentUser
) -> Any:
    """
    Get a specific user by id.
    """
    user = session.get(User, user_id)
    if user == current_user:
        return user
    if not current_user.is_superuser:
        raise HTTPException(
            status_code=403,
            detail="The user doesn't have enough privileges",
        )
    return user
