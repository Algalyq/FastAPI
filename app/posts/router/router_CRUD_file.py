from fastapi import Depends, UploadFile,status
from typing import List

from ..service import PostsService, get_service
from . import router
from ...auth.adapters.jwt_service import JWTData
from ...auth.router.dependencies import parse_jwt_user_data
from ...auth.service import Service,get_service as auth_service


@router.post("/{post_id}/media/file")
def upload_file(
    post_id: str,
    file: UploadFile,
    svc: PostsService = Depends(get_service),
    auth_svc: Service = Depends(auth_service),
    jwt_data: JWTData = Depends(parse_jwt_user_data)

):
    user = auth_svc.repository.get_user_by_id(jwt_data.user_id)
    if user:
        url = svc.s3_service.upload_file(file.file, file.filename)
    id = svc.images.create_images(post_id, url)
    if id:
        return {"msg":status.HTTP_200_OK}
    return {"msg": url}

@router.post("/{post_id}/media")
def upload_files(
    post_id: str,
    files: List[UploadFile],
    svc: PostsService = Depends(get_service),
    jwt_data: JWTData = Depends(parse_jwt_user_data)
):
    result = []
    for file in files:
        url = svc.s3_service.upload_file(file.file, file.filename)
        result.append(url)
    id = svc.images.create_images(post_id, result)
    if id:
        return {"msg":status.HTTP_200_OK}
    return {"msg":status.HTTP_400_BAD_REQUEST}


class DeleteImageRequest(AppModel):
    media: list

@router.delete("/{post_id}/media",)
def delete_images_by_post_id(
    post_id: str,
    input: DeleteImageRequest,
    jwt_data: JWTData = Depends(parse_jwt_user_data),
    svc: PostsService = Depends(get_service)
):
    post_images = svc.images.delete_images_by_post_id(post_id)
    # for i in input:
    #     if isinstance(i, tuple):
    #         i = i[0]
    #     image_name = i.split('/')[-1]
    #     svc.s3_service.delete_file(image_name)
    if post_images:
        return {"message":status.HTTP_200_OK}
    return {"message":status.HTTP_400_BAD_REQUEST}
