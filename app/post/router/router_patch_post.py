from typing import Any
from fastapi import Depends, HTTPException, status
from pydantic import Field

from app.utils import AppModel

from ...auth.adapters.jwt_service import JWTData
from ..service import PostsService, get_service
from . import router
from ...auth.router.dependencies import parse_jwt_user_data


class PostPatchRequest(AppModel):
    type: str
    price: int
    address: str
    area: float
    rooms_count: int
    description: str


@router.patch("/{post_id}")
def update_post(
    post_id: str,
    input: PostPatchRequest,
    jwt_data: JWTData = Depends(parse_jwt_user_data),
    post_service: PostsService = Depends(get_service)
):
    updated_post = post_service.repository.update_post_data(post_id, input)
    
    if update_post:
        return {"message": status.HTTP_200_OK}
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail="Post not found"
    )

