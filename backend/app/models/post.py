import uuid, datetime

from sqlmodel import SQLModel, Field, Relationship
from pydantic import BaseModel

from app.models.cat import Cat
from app.models.user import User

UTC_8 = datetime.timezone(datetime.timedelta(hours=8))


# - MARK: PostTagRelation
class PostTagRelation(SQLModel, table=True):
    """
    Link Table: Represents the many-to-many relationship between posts and tags.
    - **post_id**: Foreign key, references post ID, primary key.
    - **tag_id**: Foreign key, references tag ID, primary key.
    """
    post_id: uuid.UUID = Field(foreign_key="post.id", primary_key=True, index=True, ondelete="CASCADE")
    tag_id: uuid.UUID = Field(foreign_key="posttag.id", primary_key=True, index=True, ondelete="CASCADE")


# - MARK: Post
class Post(SQLModel, table=True):
    """
    Post Table: Stores basic information about posts.
    - id: Primary key, unique identifier for the post.
    - user_id: Foreign key, references the user ID.
    - cat_id: Foreign key, optional, references the category ID.
    - title: Title of the post.
    - content: Content of the post.
    - created_at: Creation timestamp (UTC+8).
    """
    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    user_id: uuid.UUID = Field(foreign_key="user.id", index=True)
    cat_id: uuid.UUID | None = Field(default=None, foreign_key="cat.id", nullable=True)
    title: str
    content: str = Field(max_length=8192)
    created_at: datetime.datetime = Field(default_factory=lambda: datetime.datetime.now(tz=UTC_8))
    
    # relationships
    tags: list["PostTag"] = Relationship(back_populates="posts", link_model=PostTagRelation)
    images: list["PostMedia"] = Relationship(back_populates="post", cascade_delete=True)


# - MARK: PostMedia
class PostMedia(SQLModel, table=True):
    """
    Media Table: Stores media files related to posts.
    - id: Primary key, unique identifier for the media.
    - post_id: Foreign key, references the associated post ID.
    - image_url: URL of the media file (max length 512 characters).
    """
    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    post_id: uuid.UUID = Field(foreign_key="post.id", ondelete="CASCADE")
    image_url: str = Field(max_length=512)
    
    # relationships
    post: Post = Relationship(back_populates="images")


# - MARK: PostTag    
class PostTag(SQLModel, table=True):
    """
    Tag Table: Stores information about tags.
    - id: Primary key, unique identifier for the tag.
    - user_id: Foreign key, references the user ID.
    - name: Name of the tag.
    """
    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    user_id: uuid.UUID = Field(foreign_key="user.id", index=True)
    name: str = Field(index=True)
    
    # relationships
    posts: list["Post"] = Relationship(back_populates="tags", link_model=PostTagRelation)


# - MARK: Like
class Like(SQLModel, table=True):
    """
    Like Table: Records user likes for posts.
    - user_id: Foreign key, references the user ID (the user who liked the post).
    - post_id: Foreign key, references the post ID (the liked post).
    """
    user_id: uuid.UUID = Field(foreign_key="user.id", primary_key=True, ondelete="CASCADE")
    post_id: uuid.UUID = Field(foreign_key="post.id", primary_key=True, ondelete="CASCADE")
    

# - MARK: API models
class PostPublic(BaseModel):
    """
    Represents the public-facing data for a single post.
    - id: Unique identifier for the post.
    - title: Title of the post.
    - content: Content/body of the post.
    - created_at: Timestamp indicating when the post was created.
    - likes_number: Number of likes for the post.
    - like_status: A boolean indicating whether the current user has liked the post (optional).
    - tags: A list of tag names associated with the post (optional).
    - images: A list of image URLs associated with the post (optional).
    """
    id: uuid.UUID
    user_id: uuid.UUID
    title: str
    content: str
    created_at: datetime.datetime
    likes_number: int = 0
    like_status: bool | None = None
    tags: list[str] | None = None
    images: list[str] | None = None


class PostsPublic(BaseModel):
    """
    Represents a collection of posts for public viewing.
    - posts: A list of `PostPublic` objects, each representing an individual post.
    """
    posts: list[PostPublic]
    

class PostCreate(BaseModel):
    """
    Represents the data required to create a new post.
    - title: Title of the new post.
    - content: Content/body of the new post.
    """
    title: str
    content: str


class PostUpdate(BaseModel):
    """
    Represents the data required to update an existing post. All fields are optional.
    - cat_id: ID of the new cat for the post (optional).
    - title: New title for the post (optional).
    - content: New content/body for the post (optional).
    """
    title: str | None = None
    content: str | None = None
    cat_id: uuid.UUID | None = None


class PostTagCreate(BaseModel):
    """
    Represents the data required to create a new tag.
    - name: Name of the tag to be created.
    """
    name: str


class PostTagPublic(BaseModel):
    """
    Represents the public-facing data for a single tag.
    - id: Unique identifier for the tag.
    - name: Name of the tag.
    """
    id: uuid.UUID
    name: str
