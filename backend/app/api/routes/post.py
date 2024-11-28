import uuid
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
from app.models.post import (
    Post, PostPublic, PostsPublic, PostCreate, 
    PostTag, PostTagCreate, PostTagPublic, PostMedia,
    Like
)
from app.util.utils import save_file, remove_file
from app.core.config import settings


router = APIRouter()


# - MARK: get all posts
@router.get("/", response_model=PostsPublic, dependencies=[LoginRequired])
async def get_posts(*, session: SessionDep, offset: int = 0, limit: int = 100) -> PostsPublic:
    """
    Get all posts.
    """
    posts = session.exec(
        select(Post).offset(offset).limit(limit)
    )
    response = [
        PostPublic(
            **post.model_dump(), 
            likes_number=crud.get_post_likes_count(session=session, post_id=post.id), 
            tags=[tag.name for tag in post.tags], 
            images=[image.image_url for image in post.images]
        ) for post in posts
        ]
    return PostsPublic(posts=response)


# - MARK: get post by id
@router.get("/{id}", response_model=PostPublic, dependencies=[LoginRequired])
async def get_post(*, session: SessionDep, id: uuid.UUID) -> PostPublic:
    """
    Get a post by id.
    """
    post = crud.get_post_by_id(session=session, post_id=id)
    if not post:
        raise HTTPException(status_code=404, detail="没有找到对应的帖子")
    return PostPublic.model_validate(post.model_dump())


# - MARK: create post
@router.post("/", response_model=PostPublic)
async def create_post(
    *, 
    session: SessionDep, 
    current_user: CurrentUser, 
    post_in: PostCreate = Depends(), 
    tags: List[str] = Form(...),
    upload_images: list[UploadFile] = File(...)
) -> PostPublic:
    """
    Create a new post.
    """
    post = Post(**post_in.model_dump())
    post.user_id = current_user.id
    # TODO: link with cats
    for tag in tags:
        if session.exec(select(PostTag).where(PostTag.name == tag)).first():
            raise HTTPException(status_code=400, detail="该标签已存在")
        post.tags.append(PostTag(name=tag, user_id=current_user.id))
        
    for image in upload_images:
        file_url = save_file(settings.UPLOAD_POST_IMAGE_FOLDER, image, current_user.email)
        post.images.append(PostMedia(post_id=post.id, image_url=file_url))
        
    session.add(post)
    session.commit()
    session.refresh(post)
    
    response = PostPublic(**post.model_dump())
    response.tags = [tag.name for tag in post.tags]
    response.images = [image.image_url for image in post.images]
    # TODO: images
    
    return response


# - MARK: like post
@router.post("/{id}/like")
async def like_post(*, session: SessionDep, current_user: CurrentUser, post_id: uuid.UUID):
    """
    Successfully return schema: 
    ```
    {"message": string, "likes_number": int}
    ```
    """
    if session.exec(select(Like).where(Like.user_id == current_user.id, Like.post_id == post_id)).first():
        raise HTTPException(status_code=400, detail="不能重复点赞")
    new_like = Like(user_id=current_user.id, post_id=post_id)
    session.add(new_like)
    session.commit()
    session.refresh(new_like)
    return JSONResponse(status_code=200, content={"message": "点赞成功", "likes_number": crud.get_post_likes_count(session=session, post_id=post_id)})


# - MARK: delete post
@router.delete("/{id}", dependencies=[LoginRequired])
async def delete_post(*, session: SessionDep, current_user: CurrentUser, post_id: uuid.UUID):
    """
    Delete a post by id.
    """
    post = crud.get_post_by_id(session=session, post_id=post_id)
    if not post:
        raise HTTPException(status_code=404, detail="Post not found")
    if post.user_id != current_user.id:
        raise HTTPException(status_code=403, detail="Forbidden")
    for image in post.images:
        remove_file(settings.UPLOAD_POST_IMAGE_FOLDER, image.image_url)
    session.delete(post)
    session.commit()
    return JSONResponse(status_code=200, content={"message": "删除成功"})