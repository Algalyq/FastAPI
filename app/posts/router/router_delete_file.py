from typing import Any
from fastapi import Depends, HTTPException, status
from pydantic import Field

from app.utils import AppModel

from ...auth.adapters.jwt_service import JWTData
from ..service import PostsService, get_service
from . import router
from ...auth.router.dependencies import parse_jwt_user_data



@router.delete("/{post_id}/media",)
def delete_images_by_post_id(
    post_id: str,
    jwt_data: JWTData = Depends(parse_jwt_user_data),
    svc: PostsService = Depends(get_service)
):
    post_images = svc.images.delete_images_by_post_id(post_id)
    
    if post_images:
        return {"message":status.HTTP_200_OK}
    return {"message":status.HTTP_400_BAD_REQUEST}
