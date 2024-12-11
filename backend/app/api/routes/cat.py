import uuid, logging
from typing import List

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
    CatLocationCreate, CatLocationPublic, CatMedia
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
            latest_latitude=getattr(crud.get_latest_cat_location(session, cat.id), 'latitude', None),
            image_urls=[img.image_url for img in cat.images]
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
        latest_latitude=getattr(crud.get_latest_cat_location(session, cat.id), 'latitude', None),
        image_urls=[img.image_url for img in cat.images]
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
    name: str = Form(..., max_length=128), 
    is_male: bool = Form(...), 
    age: int = Form(..., ge=0, le=30), 
    health_condition: int = Form(default=1, ge=1, le=4),
    description: str | None = Form(default=None, max_length=256),
    longitude: float | None = Form(default=None),
    latitude: float | None = Form(default=None),
    image: list[UploadFile] | None = File(default=None)
) -> CatPublic:
    """
    Create cat
    """
    if session.exec(select(Cat).where(Cat.name == name)).first():
        raise HTTPException(status_code=400, detail="Cat already exists")
    
    cat = Cat(
        name=name,
        is_male=is_male,
        age=age,
        health_condition=health_condition,
        description=description
    )
    
    if longitude and latitude:
        new_location = CatLocationCreate(longitude=longitude, latitude=latitude)
        location_to_save = CatLocation(**new_location.model_dump())
        location_to_save.user_id = current_user.id
        location_to_save.cat_ref = cat
        cat.locations.append(location_to_save)
    
    if image:
        for img in image:
            file_path = save_file(settings.UPLOAD_CAT_IMAGE_FOLDER, img, current_user.email)
            new_media = CatMedia(cat_id=cat.id, image_url=file_path)
            cat.images.append(new_media)
            new_media.cat_ref = cat
    
    session.add(cat)
    session.commit()
    session.refresh(cat)
    
    return CatPublic(
        **cat.model_dump(),
        latest_longitude=getattr(crud.get_latest_cat_location(session, cat.id), 'longitude', None),
        latest_latitude=getattr(crud.get_latest_cat_location(session, cat.id), 'latitude', None),
        image_urls=[img.image_url for img in cat.images]
    )
    
    
# - MARK: Update cat info
@router.patch("/{cat_id}/info", response_model=CatPublic)
async def update_cat_info(
    session: SessionDep, 
    current_user: CurrentUser, 
    cat_id: uuid.UUID, 
    name: str | None = Form(default=None, max_length=128), 
    is_male: bool | None = Form(default=None), 
    age: int | None = Form(default=None, ge=0, le=30), 
    health_condition: int | None = Form(default=None, ge=1, le=4),
    description: str | None = Form(default=None, max_length=256),
    new_images: list[UploadFile] | None = File(default=None)
) -> CatPublic:
    """
    Update cat info
    """
    cat = session.exec(select(Cat).where(Cat.id == cat_id)).first()
    if not cat:
        raise HTTPException(status_code=404, detail="Cat not found")
    
    if name and session.exec(select(Cat).where(Cat.name == name)).first():
        raise HTTPException(status_code=400, detail="Cat already exists")
    
    cat_in_data = CatUpdateInfo(
        name=name,
        is_male=is_male,
        age=age,
        health_condition=health_condition,
        description=description
    )
    for key, value in cat_in_data.model_dump(exclude_none=True).items():
        setattr(cat, key, value)
    
    for old_img in cat.images:
        remove_file(settings.UPLOAD_CAT_IMAGE_FOLDER, old_img.image_url.split('/')[-1])
    
    # NOTE: cannot delete items while iterating
    cat.images.clear()
    
    if new_images:
        for img in new_images:
            file_path = save_file(settings.UPLOAD_CAT_IMAGE_FOLDER, img, current_user.email)
            new_media = CatMedia(cat_id=cat.id, image_url=file_path)
            cat.images.append(new_media)
            new_media.cat_ref = cat
    
    session.add(cat)
    session.commit()
    session.refresh(cat)
    
    return CatPublic(
        **cat.model_dump(),
        latest_longitude=getattr(crud.get_latest_cat_location(session, cat.id), 'longitude', None),
        latest_latitude=getattr(crud.get_latest_cat_location(session, cat.id), 'latitude', None),
        image_urls=[img.image_url for img in cat.images]
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
        latest_latitude=location_to_save.latitude,
        image_urls=[img.image_url for img in cat.images]
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