from typing import Any
from fastapi import Depends, HTTPException, status,Query
from pydantic import Field
from app.utils import AppModel
from ...auth.adapters.jwt_service import JWTData
from ..service import Service, get_service
from . import router
from ...auth.router.dependencies import parse_jwt_user_data,parse_jwt_moderator_data

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
    if post and post["approve"] == True:
        return PostGetResponse(**post)
    
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail="Post not found"
    )

# class PostGetResponse2(AppModel):
#     id: Any = Field(alias="_id")
#     type: str
#     price: int
#     address: str
#     area: float
#     rooms_count: int
#     description: str
#     media: list

@router.get("/all/")
def get_post(
    svc: Service = Depends(get_service)
):
    post = svc.repository.get_post_approved()

    if post:
        return post
    
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


class SearchPagGetResponse(AppModel):
    total: int
    objects: list

@router.get("/")
def search_pagination(
    svc: Service = Depends(get_service),
    limit: int = Query(10, gt=0, description="Number of records to display per page"),
    offset: int = Query(0, ge=0, description="Starting point for displaying data"),
    type: str = Query(None, description="Type of advertisement: sell or rent"),
    rooms_count: int = Query(None, gt=0, description="Number of rooms"),
    price_from: float = Query(None, ge=0, description="Minimum price"),
    price_until: float = Query(None, gt=0, description="Maximum price"), 
    latitude: float = Query(None,description="Latitude"),
    longitude: float = Query(None,description="Longitude"),
    radius: float = Query(None,description="Raduis")
    ):


    
    query = {}
    if type:
        query["type"] = type
    if rooms_count:
        query["rooms_count"] = rooms_count
    if price_from:
        query["price"] = {"$gte": price_from}
    if price_until:
        query.setdefault("price", {}).update({"$lte": price_until})
    
    posts = svc.repository.search_pagination(query, offset, limit,latitude,longitude,radius)
    for post in posts["objects"]:
        location = svc.here_service.get_coordinates(post["address"])
        post["location"] = location
    
    return posts

class ReviewGetResponse(AppModel):
    total: int
    objects: list

@router.get("/review/",response_model=ReviewGetResponse)
def review_approve(
    svc: Service = Depends(get_service),
    limit: int = Query(10, gt=0, description="Number of records to display per page"),
    offset: int = Query(0, ge=0, description="Starting point for displaying data"),
    jwt_data: JWTData = Depends(parse_jwt_moderator_data),
   ):
    result = svc.repository.get_post_to_approve(offset, limit)
    
    return ReviewGetResponse(total=len(result),objects=result)


@router.post("/{id}/approve")
def review_approve(
    id: str,
    svc: Service = Depends(get_service),
    jwt_data: JWTData = Depends(parse_jwt_user_data),
   ):
    
    result = svc.repository.update_to_approve(id)

    if result:
        return {"msg":status.HTTP_200_OK}
    return {"msg":status.HTTP_400_BAD_REQUEST}




@router.post("/{id}/decline")
def review_decline(
    id: str,
    svc: Service = Depends(get_service),
    jwt_data: JWTData = Depends(parse_jwt_user_data),
   ):
    result = svc.repository.update_to_decline(id)
    if result:
        return {"msg":status.HTTP_200_OK}
    return {"msg":status.HTTP_400_BAD_REQUEST}

