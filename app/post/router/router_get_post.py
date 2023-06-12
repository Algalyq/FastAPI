from typing import Any
from fastapi import Depends, HTTPException, status
from pydantic import Field

from app.utils import AppModel

from ..service import PostsService, get_service
from . import router


class PostGetResponse(AppModel):
    id: Any = Field(alias="_id")
    type: str
    price: int
    address: str
    area: float
    rooms_count: int
    description: str


@router.get("/{post_id}", response_model=PostGetResponse)
def get_post_id(
    post_id: str,
    post_service: PostsService = Depends(get_service)
):
    post = post_service.repository.get_post_by_id(post_id)
    
    if post:
        return PostGetResponse(**post)
    
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail="Post not found"
    )
