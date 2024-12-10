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
from app.models.post import (
    Post, PostPublic, PostsPublic, PostTagCreate, 
    PostTag, PostUpdate, PostTagPublic, PostMedia,
    Like
)
from app.util.utils import save_file, remove_file
from app.core.config import settings


logger = logging.getLogger(__name__)


router = APIRouter()


# - MARK: get all posts
@router.get("/", response_model=PostsPublic)
async def get_posts(*, session: SessionDep, current_user: CurrentUser, offset: int = 0, limit: int = 100) -> PostsPublic:
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
            like_status=crud.get_like_status(session=session, user_id=current_user.id, post_id=post.id),
            tags=[tag.name for tag in post.tags], 
            images=[image.image_url for image in post.images]
        ) for post in posts
    ]
    return PostsPublic(posts=response)


# - MARK: get my posts
@router.get("/my", response_model=PostsPublic)
async def get_my_posts(*, session: SessionDep, current_user: CurrentUser, offset: int = 0, limit: int = 100) -> PostsPublic:
    """
    Get all posts created by the current user.
    """
    posts = session.exec(
        select(Post).where(Post.user_id == current_user.id).offset(offset).limit(limit)
    )
    response = [
        PostPublic(
            **post.model_dump(), 
            likes_number=crud.get_post_likes_count(session=session, post_id=post.id),
            like_status=crud.get_like_status(session=session, user_id=current_user.id, post_id=post.id),
            tags=[tag.name for tag in post.tags], 
            images=[image.image_url for image in post.images]
        ) for post in posts
    ]
    return PostsPublic(posts=response)


# - MARK: return all tags
@router.get("/tags", response_model=list[PostTagPublic], dependencies=[LoginRequired])
async def get_tags(*, session: SessionDep) -> list[PostTagPublic]:
    """
    Get all tags for creating a new post.
    """
    tags = session.exec(select(PostTag)).all()
    return [PostTagPublic(**tag.model_dump()) for tag in tags]


# - MARK: get post by id
@router.get("/{id}", response_model=PostPublic)
async def get_post(*, session: SessionDep, current_user: CurrentUser, id: uuid.UUID) -> PostPublic:
    """
    Get a post by id.
    """
    post = session.get(Post, id)
    if not post:
        raise HTTPException(status_code=404, detail="没有找到对应的帖子")
    response = PostPublic(
        **post.model_dump(), 
        likes_number=crud.get_post_likes_count(session=session, post_id=post.id), 
        # only show like status in post detail view
        like_status=crud.get_like_status(session=session, user_id=current_user.id, post_id=post.id), 
        tags=[tag.name for tag in post.tags], 
        images=[image.image_url for image in post.images]
    )
    return response


# - MARK: create post
@router.post("/", response_model=PostPublic)
async def create_post(
    *, 
    session: SessionDep, 
    current_user: CurrentUser, 
    title: str = Form(...), 
    content: str = Form(...), 
    tags: List[str] | None = Form(default=None),
    upload_images: list[UploadFile] | None = File(default=None)
) -> PostPublic:
    """
    Create a new post.
    # 重要:
    ### 如果选择的tag为空也**必须保留tag字段**，但是如果上传文件为空则不需要保留upload_images字段!
    """
    post = Post(title=title, content=content, user_id=current_user.id)
    # TODO: link with cats
    if tags:
        logger.info(f"tags: {tags}")
        for tag in tags:
            for tag_name in tag.split(","):
                exist_tag = session.exec(select(PostTag).where(PostTag.name == tag_name)).first()
                if exist_tag:
                    post.tags.append(exist_tag)
                else:
                    post.tags.append(PostTag(name=tag_name, user_id=current_user.id)) if len(tag_name) > 0 else None
    
    if upload_images:
        for image in upload_images:
            file_url = save_file(settings.UPLOAD_POST_IMAGE_FOLDER, image, current_user.email)
            post.images.append(PostMedia(post_id=post.id, image_url=file_url))
        
    session.add(post)
    session.commit()
    session.refresh(post)
    
    response = PostPublic(**post.model_dump())
    response.tags = [tag.name for tag in post.tags]
    response.images = [image.image_url for image in post.images]
    response.like_status = False
    # TODO: should I return all tags?
    
    return response


# - MARK: sudo create tag
@router.post("/tags", response_model=PostTagPublic, dependencies=[Depends(get_current_superuser)], tags=["superuser"])
async def create_tag_by_superuser(
    session: SessionDep, current_user: CurrentUser, tag_in: PostTagCreate
) -> PostTagPublic:
    """
    Create a new tag by superuser
    """
    tag = PostTag(name=tag_in.name, user_id=current_user.id)
    session.add(tag)
    session.commit()
    session.refresh(tag)
    return PostTagPublic(**tag.model_dump())


# - MARK: update post
@router.patch("/{id}", response_model=PostPublic)
async def update_post(
    *, 
    session: SessionDep, 
    current_user: CurrentUser, 
    id: uuid.UUID, 
    title: str | None = Form(default=None), 
    content: str | None = Form(default=None), 
    tags: List[str] | None = Form(default=None),
    keep_images: List[str] | None = Form(default=None),
    upload_images: list[UploadFile] | None = File(default=None)
) -> PostPublic:
    """
    Update a post by id.

    ### Parameters
    1. **Path Parameter**:
    - `id` (UUID): The unique identifier of the post to update.

    2. **Form Data**:
    - `title` (str | None): The new title of the post. If omitted, the title remains unchanged.
    - `content` (str | None): The new content of the post. If omitted, the content remains unchanged.
    - `tags` (List[str]): A list of tag names to associate with the post. The previous tags will be replaced with this list.
    - `keep_images` (List[str]): A list of URLs representing images to retain from the current post. Any image not listed here will be removed.
    
    3. **File Uploads**:
    - `upload_images` (List[UploadFile]): A list of new image files to upload and associate with the post.

    ### Example Request Data
    #### Form Fields:
    ```
    {
        "title": "Updated Post Title",
        "content": "Updated content of the post.",
        "tags": ["tag1", "tag2", "tag3"],
        "keep_images": [
            "/static/uploads/posts/image1.jpg",
            "/static/uploads/posts/image2.jpg"
        ]
    }
    ```
    """
    post = session.get(Post, id)
    if not post:
        raise HTTPException(status_code=404, detail="Post not found")
    post.title = title or post.title
    post.content = content or post.content
    post.tags.clear()
    if tags:
        for tag in tags:
            for tag_name in tag.split(","):
                exist_tag = session.exec(select(PostTag).where(PostTag.name == tag_name)).first()
                if exist_tag:
                    logger.info(f"exist_tag: {exist_tag.name}")
                    post.tags.append(exist_tag)
                else:
                    logger.info(f"new_tag: {tag_name}")
                    post.tags.append(PostTag(name=tag_name, user_id=current_user.id)) if len(tag_name) > 0 else None
    
    if not keep_images:
        for image in post.images:
            remove_file(image.image_url)
            session.delete(image)
    else:
        for old_image in post.images:
            if old_image.image_url not in keep_images:
                # remove discarded image file
                remove_file(old_image.image_url)
                # remove image record from database
                session.delete(old_image)
    
    if upload_images:
        for image in upload_images:
            file_url = save_file(settings.UPLOAD_POST_IMAGE_FOLDER, image, current_user.email)
            post.images.append(PostMedia(post_id=post.id, image_url=file_url))
    
    session.add(post)
    session.commit()
    session.refresh(post)
    
    response = PostPublic(**post.model_dump())
    response.tags = [tag.name for tag in post.tags]
    response.images = [image.image_url for image in post.images]
    # Notice that like_status and likes_number are not included in the response, use the old values instead
    return response


# - MARK: sudo delete tag
@router.delete("/tags/{tag_id}", dependencies=[Depends(get_current_superuser)], tags=["superuser"])
async def delete_tag_by_superuser(*, session: SessionDep, tag_id: uuid.UUID):
    """
    Delete a tag by superuser
    """
    tag = session.get(PostTag, tag_id)
    if not tag:
        raise HTTPException(status_code=404, detail="Tag not found")
    session.delete(tag)
    session.commit()
    return JSONResponse(status_code=200, content={"message": "删除成功"})


# - MARK: delete post
@router.delete("/{id}")
async def delete_post(*, session: SessionDep, current_user: CurrentUser, id: uuid.UUID):
    """
    Delete a post by id.
    """
    post = session.get(Post, id)
    if not post:
        raise HTTPException(status_code=404, detail="Post not found")
    if post.user_id != current_user.id:
        if not current_user.is_superuser:
            raise HTTPException(status_code=403, detail="Forbidden")
    for image in post.images:
        remove_file(image.image_url)
    session.delete(post)
    session.commit()
    return JSONResponse(status_code=200, content={"message": "删除成功"})


# - MARK: like post
@router.post("/{id}/like")
async def like_post(*, session: SessionDep, current_user: CurrentUser, id: uuid.UUID):
    """
    Successfully return schema: 
    ```
    {"message": string, "likes_number": int}
    ```
    """
    if session.exec(select(Like).where(Like.user_id == current_user.id, Like.post_id == id)).first():
        raise HTTPException(status_code=400, detail="不能重复点赞")
    new_like = Like(user_id=current_user.id, post_id=id)
    session.add(new_like)
    session.commit()
    session.refresh(new_like)
    return JSONResponse(status_code=200, content={"message": "点赞成功", "likes_number": crud.get_post_likes_count(session=session, post_id=id)})


# - MARK: unlike post
@router.delete("/{id}/like")
async def unlike_post(*, session: SessionDep, current_user: CurrentUser, id: uuid.UUID):
    """
    Successfully return schema: 
    ```
    {"message": string, "likes_number": int}
    ```
    """
    if not session.exec(select(Like).where(Like.user_id == current_user.id, Like.post_id == id)).first():
        raise HTTPException(status_code=400, detail="您还没有点赞过该帖")
    like = session.get(Like, (current_user.id, id))
    session.delete(like)
    session.commit()
    return JSONResponse(status_code=200, content={"message": "取消点赞成功", "likes_number": crud.get_post_likes_count(session=session, post_id=id)})
