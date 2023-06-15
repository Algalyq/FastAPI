from fastapi import Depends, UploadFile,status
from app.utils import AppModel
from ..service import Service, get_service
from . import router
from ..adapters.jwt_service import JWTData
from .dependencies import parse_jwt_user_data


@router.post("/users/me")
def add_avatar_user(
    file: UploadFile,
    svc: Service = Depends(get_service),
    jwt_data: JWTData = Depends(parse_jwt_user_data)
):
    url = svc.s3_service.upload_file(file.file, file.filename)

    result = svc.repository.post_avatar_user(jwt_data.user_id, url)


    if result:
        return {"msg":status.HTTP_200_OK}
    return {"msg":status.HTTP_400_BAD_REQUEST}

@router.delete("/users/avatar")
def delete_avatar_user(
    svc: Service = Depends(get_service),
    jwt_data: JWTData = Depends(parse_jwt_user_data)
    ):
    result = svc.repository.delete_avatar_user(jwt_data.user_id)
    if result:
        return {"message":status.HTTP_200_OK}
    return {"message":"Not found"}
    

