from typing import Any
from fastapi import Depends, HTTPException, status
from pydantic import Field

from app.utils import AppModel

from ...auth.adapters.jwt_service import JWTData
from ...auth.service import Service,get_service as auth_service
from ..service import PostsService, get_service
from . import router
from ...auth.router.dependencies import parse_jwt_user_data


class CommentUpdateRequest(AppModel):
    content: str


@router.patch("/{post_id}/comments/{comment_id}")
def update_post(
    post_id: str,
    comment_id: str,
    input: CommentUpdateRequest,
    jwt_data: JWTData = Depends(parse_jwt_user_data), 
    auth_svc: Service = Depends(auth_service),
    svc: PostsService = Depends(get_service)
):  
    user = auth_svc.repository.get_user_by_id(jwt_data.user_id)
    if user:
        updated_post = svc.comment.update_comment(comment_id, input.content)
        if update_post:
            return {"message": status.HTTP_200_OK}
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail="Post not found"
    )

