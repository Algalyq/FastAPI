from typing import Any
from fastapi import Depends, HTTPException, status
from pydantic import Field

from app.utils import AppModel

from ...auth.adapters.jwt_service import JWTData
from ..service import PostsService, get_service
from . import router
from ...auth.router.dependencies import parse_jwt_user_data



@router.delete("/{post_id}",)
def delete_post_id(
    post_id: str,
    jwt_data: JWTData = Depends(parse_jwt_user_data),
    post_service: PostsService = Depends(get_service)
):
    post = post_service.repository.delete_post_by_id(post_id)
    
    if post:
        return {"message":status.HTTP_200_OK}
    return {"message":status.HTTP_400_BAD_REQUEST}
