from typing import Any
from fastapi import Depends, HTTPException, status
from pydantic import Field

from app.utils import AppModel

from ...auth.adapters.jwt_service import JWTData
from ...auth.service import Service,get_service as auth_service
from ..service import PostsService, get_service
from . import router
from ...auth.router.dependencies import parse_jwt_user_data



@router.delete("/{post_id}/comments/{comment_id}",)
def delete_images_by_post_id(
    post_id: str,  
    comment_id: str,
    svc: PostsService = Depends(get_service),
    auth_svc: Service = Depends(auth_service),
    jwt_data: JWTData = Depends(parse_jwt_user_data),
    ):
    user = auth_svc.repository.get_user_by_id(jwt_data.user_id)
    if user:
        comment = svc.comment.delete_comment(comment_id)
        if comment:
            return {"message":status.HTTP_200_OK}
        return {"message":"Not found comment"}
    return {"message":"User not found"}
