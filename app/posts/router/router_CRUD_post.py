from typing import Any
from fastapi import Depends, HTTPException, status
from pydantic import Field
from app.utils import AppModel
from ...auth.adapters.jwt_service import JWTData
from ..service import Service, get_service
from . import router
from ...auth.router.dependencies import parse_jwt_user_data


class PostGetResponse(AppModel):
    id: Any = Field(alias="_id")
    type: str
    price: int
    address: str
    area: float
    rooms_count: int
    description: str
    media: list
    location: dict

@router.get("/{post_id}", response_model=PostGetResponse)
def get_post_id(
    post_id: str,
    svc: Service = Depends(get_service)
):
    post = svc.repository.get_post_by_id(post_id)
    location = svc.here_service.get_coordinates(post["address"])
    post["location"] = location
    if post:
        return PostGetResponse(**post)
    
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail="Post not found"
    )



class PostCreateRequest(AppModel):
    type: str
    price: int
    address: str
    area: float
    rooms_count: int
    description: str

class PostCreateResponse(AppModel):
    id : str

@router.post("/",response_model=PostCreateResponse,status_code=status.HTTP_201_CREATED)
def create_post(input: PostCreateRequest,svc: Service = Depends(get_service),):
    
    id = svc.repository.create_post(input.dict())
    
    return PostCreateResponse(id=id)




class PostPatchRequest(AppModel):
    type: str
    price: int
    address: str
    area: float
    rooms_count: int
    description: str


@router.patch("/{post_id}")
def update_post(
    post_id: str,
    input: PostPatchRequest,
    jwt_data: JWTData = Depends(parse_jwt_user_data),
    svc: Service = Depends(get_service)
):  
    updated_post = svc.repository.update_post_data(post_id, input)
    
    if update_post:
        return {"message": status.HTTP_200_OK}
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail="Post not found"
    )



@router.delete("/{post_id}",)
def delete_post_id(
    post_id: str,
    jwt_data: JWTData = Depends(parse_jwt_user_data),
    svc: Service = Depends(get_service)
):
    post = svc.repository.delete_post_by_id(post_id)
    
    if post:
        return {"message":status.HTTP_200_OK}
    return {"message":status.HTTP_400_BAD_REQUEST}
