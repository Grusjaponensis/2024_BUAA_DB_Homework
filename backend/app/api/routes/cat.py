import uuid, logging

from fastapi import (
    APIRouter, HTTPException, Depends, 
    File, UploadFile, Form
)
from fastapi.responses import JSONResponse
from sqlmodel import select, func

import app.crud as crud
from app.api.deps import (
    LoginRequired,
    CurrentUser,
    SessionDep,
    get_current_superuser
)
from app.models.cat import (
    Cat, CatCreate, CatLocation, CatPublic, 
    CatUpdateInfo, CatUpdateLocation, CatsPublic,
    CatLocationCreate, CatLocationPublic
)
from app.util.utils import save_file, remove_file
from app.core.config import settings


logger = logging.getLogger(__name__)


router = APIRouter()


# - MARK: Get all cats
@router.get("/", response_model=CatsPublic, dependencies=[LoginRequired])
async def get_cats(session: SessionDep, offset: int = 0, limit: int = 100) -> CatsPublic:
    """
    Get all cats
    """
    cats = session.exec(select(Cat).offset(offset).limit(limit))
    response = [
        CatPublic(
            **cat.model_dump(),
            latest_longitude=getattr(crud.get_latest_cat_location(session, cat.id), 'longitude', None),
            latest_latitude=getattr(crud.get_latest_cat_location(session, cat.id), 'latitude', None)
        ) for cat in cats
    ]
    
    return CatsPublic(cats=response)


# - MARK: Get cat by id
@router.get("/{cat_id}", response_model=CatPublic, dependencies=[LoginRequired])
async def get_cat_by_id(session: SessionDep, cat_id: uuid.UUID) -> CatPublic:
    """
    Get cat by id
    """
    cat = session.exec(select(Cat).where(Cat.id == cat_id)).first()
    if not cat:
        raise HTTPException(status_code=404, detail="Cat not found")
    
    return CatPublic(
        **cat.model_dump(),
        latest_longitude=getattr(crud.get_latest_cat_location(session, cat.id), 'longitude', None),
        latest_latitude=getattr(crud.get_latest_cat_location(session, cat.id), 'latitude', None)
    )
    

# - MARK: Get cat locs
@router.get("/{cat_id}/locations", response_model=list[CatLocationPublic])
async def get_cat_locations(session: SessionDep, cat_id: uuid.UUID):
    """
    Get cat locations
    """
    cat = session.exec(select(Cat).where(Cat.id == cat_id)).first()
    if not cat:
        raise HTTPException(status_code=404, detail="Cat not found")
    
    return [CatLocationPublic(**location.model_dump()) for location in cat.locations]



# - MARK: Create cat
@router.post("/", response_model=CatPublic)
async def create_cat(
    session: SessionDep, 
    current_user: CurrentUser, 
    cat_in: CatCreate, 
    location_in: CatLocationCreate | None = None
) -> CatPublic:
    """
    Create cat
    """
    new_name = cat_in.name
    if session.exec(select(Cat).where(Cat.name == new_name)).first():
        raise HTTPException(status_code=400, detail="Cat already exists")
    
    cat = Cat.model_validate(cat_in)
    if location_in:
        location_to_save = CatLocation(**location_in.model_dump())
        location_to_save.user_id = current_user.id
        location_to_save.cat_ref = cat
        cat.locations.append(location_to_save)
    
    session.add(cat)
    session.commit()
    session.refresh(cat)
    
    return CatPublic(
        **cat.model_dump(),
        latest_longitude=getattr(crud.get_latest_cat_location(session, cat.id), 'longitude', None),
        latest_latitude=getattr(crud.get_latest_cat_location(session, cat.id), 'latitude', None)
    )
    
    
# - MARK: Update cat info
@router.patch("/{cat_id}/info", response_model=CatPublic, dependencies=[LoginRequired])
async def update_cat_info(
    session: SessionDep, 
    cat_id: uuid.UUID, 
    cat_in: CatUpdateInfo
) -> CatPublic:
    """
    Update cat info
    """
    cat = session.exec(select(Cat).where(Cat.id == cat_id)).first()
    if not cat:
        raise HTTPException(status_code=404, detail="Cat not found")
    
    cat_in_data = cat_in.model_dump(exclude_unset=True)
    for key, value in cat_in_data.items():
        setattr(cat, key, value)
    
    session.add(cat)
    session.commit()
    session.refresh(cat)
    
    return CatPublic(
        **cat.model_dump(),
        latest_longitude=getattr(crud.get_latest_cat_location(session, cat.id), 'longitude', None),
        latest_latitude=getattr(crud.get_latest_cat_location(session, cat.id), 'latitude', None)
    )
    
    
# - MARK: Update cat loc
@router.patch("/{cat_id}/location", response_model=CatPublic)
async def update_cat_location(
    session: SessionDep, 
    current_user: CurrentUser, 
    cat_id: uuid.UUID, 
    location_in: CatLocationCreate
) -> CatPublic:
    """
    Update cat location
    """
    cat = session.exec(select(Cat).where(Cat.id == cat_id)).first()
    if not cat:
        raise HTTPException(status_code=404, detail="Cat not found")
    
    location_to_save = CatLocation(**location_in.model_dump())
    location_to_save.user_id = current_user.id
    location_to_save.cat_ref = cat
    cat.locations.append(location_to_save)
    
    session.add(cat)
    session.commit()
    session.refresh(cat)
    
    return CatPublic(
        **cat.model_dump(),
        latest_longitude=location_to_save.longitude,
        latest_latitude=location_to_save.latitude
    )
    
    
# - MARK: superuser actions
@router.delete("/{cat_id}", dependencies=[Depends(get_current_superuser)])
async def delete_cat(
    session: SessionDep, 
    cat_id: uuid.UUID
) -> JSONResponse:
    """
    Delete cat, return status code 200 if success
    """
    cat = session.exec(select(Cat).where(Cat.id == cat_id)).first()
    if not cat:
        raise HTTPException(status_code=404, detail="Cat not found")
    
    session.delete(cat)
    session.commit()
    
    return JSONResponse(status_code=200, content={"message": "Cat deleted successfully"})


# Adoption...