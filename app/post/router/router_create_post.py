from fastapi import Depends, HTTPException, status

from app.utils import AppModel

from ..service import PostsService, get_service
from . import router


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
def create_post(input: PostCreateRequest,svc_post: PostsService = Depends(get_service),):
    
    id = svc_post.repository.create_post(input.dict())
    
    return PostCreateResponse(id=id)