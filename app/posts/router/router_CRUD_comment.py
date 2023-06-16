from typing import Any
from fastapi import Depends, HTTPException, status
from pydantic import Field

from app.utils import AppModel

from ...auth.adapters.jwt_service import JWTData
from ...auth.service import Service,get_service as auth_service
from ..service import Service as PostService,get_service
from . import router
from ...auth.router.dependencies import parse_jwt_user_data


class CommentGetResponse(AppModel):
    comments: list

@router.get("/{post_id}/comments",response_model=CommentGetResponse)
def get_comments(
    post_id: str,
    svc: PostService = Depends(get_service),
    auth_svc: Service = Depends(auth_service),
    jwt_data: JWTData = Depends(parse_jwt_user_data),
):

    result = svc.comment.get_comments(post_id)

    return CommentGetResponse(comments=result)
    


class CommentCreateRequest(AppModel):
    content: str


@router.post("/{post_id}/comments")
def create_comment(
    post_id: str,   
    input: CommentCreateRequest,
    svc: PostService = Depends(get_service),
    auth_svc: Service = Depends(auth_service),
    jwt_data: JWTData = Depends(parse_jwt_user_data),
    ):
    
    user = auth_svc.repository.get_user_by_id(jwt_data.user_id)
    if user:
        id = svc.comment.create_comment(post_id, jwt_data.user_id, input.content)
        if id:
            return {"msg":status.HTTP_200_OK}
        return {"msg":"User not found"}
    return {"msg":status.HTTP_400_BAD_REQUEST}


@router.delete("/{post_id}/comments/{comment_id}",)
def delete_images_by_post_id(
    post_id: str,  
    comment_id: str,
    svc: PostService = Depends(get_service),
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


class CommentUpdateRequest(AppModel):
    content: str


@router.patch("/{post_id}/comments/{comment_id}")
def update_comment(
    post_id: str,
    comment_id: str,
    input: CommentUpdateRequest,
    jwt_data: JWTData = Depends(parse_jwt_user_data), 
    auth_svc: Service = Depends(auth_service),
    svc: PostService = Depends(get_service)
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

