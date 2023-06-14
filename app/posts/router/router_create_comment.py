from fastapi import Depends, HTTPException, status

from app.utils import AppModel
from ...auth.service import Service,get_service as auth_service
from ..service import PostsService, get_service
from . import router
from ...auth.router.dependencies import parse_jwt_user_data

from ...auth.adapters.jwt_service import JWTData


class CommentCreateRequest(AppModel):
    content: str


@router.post("/{post_id}/comments")
def create_comment(
    post_id: str,   
    input: CommentCreateRequest,
    svc: PostsService = Depends(get_service),
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
