from fastapi import Depends,status
from app.utils import AppModel
from ...posts.service import Service as PostService, get_service as post_service
from ..service import Service, get_service
from . import router
from ..adapters.jwt_service import JWTData
from .dependencies import parse_jwt_user_data

@router.post("/users/favorites/shanyraks/{id}")
def add_to_fav(
    id: str,
    svc: Service = Depends(get_service),
    post_svc: PostService = Depends(post_service),
    jwt_data: JWTData = Depends(parse_jwt_user_data)
):
    result = svc.favorites.create_fav(jwt_data.user_id, post_svc.repository.get_post_by_id(id)["address"] )
    if result:
        return {"msg":status.HTTP_200_OK}
    return {"msg":status.HTTP_400_BAD_REQUEST}

class GetFavResponse(AppModel):
    shanyraks: list

@router.get("/users/favorites/shanyraks",response_model=GetFavResponse)
def get_favorites(
    svc: Service = Depends(get_service),
    jwt_data: JWTData = Depends(parse_jwt_user_data)
):
    result = svc.favorites.get_favorites(jwt_data.user_id)
    
    return GetFavResponse(shanyraks=result)

@router.delete("/users/favorites/shanyraks/{id}")
def delete_favorite(
    id: str,
    svc: Service = Depends(get_service),
    jwt_data: JWTData = Depends(parse_jwt_user_data)
    ):
    user = svc.repository.get_user_by_id(jwt_data.user_id)
    if user:
        fav = svc.favorites.delete_favorites(id)
        if fav:
            return {"message":status.HTTP_200_OK}
        return {"message":"Not found fav"}
    return {"message":"User not found"}