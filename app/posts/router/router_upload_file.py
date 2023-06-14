from fastapi import Depends, UploadFile,status
from typing import List

from ..service import PostsService, get_service
from . import router
from ...auth.adapters.jwt_service import JWTData
from ...auth.router.dependencies import parse_jwt_user_data


@router.post("/{post_id}/media/file")
def upload_file(
    post_id: str,
    file: UploadFile,
    svc: PostsService = Depends(get_service),
    jwt_data: JWTData = Depends(parse_jwt_user_data)

):
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
    """
    file.filename: str - Название файла
    file.file: BytesIO - Содержимое файла
    """
    result = []
    for file in files:
        url = svc.s3_service.upload_file(file.file, file.filename)
        result.append(url)
    id = svc.images.create_images(post_id, result)
    if id:
        return {"msg":status.HTTP_200_OK}
    return {"msg":status.HTTP_400_BAD_REQUEST}