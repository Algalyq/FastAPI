from fastapi import Depends, HTTPException, status

from app.utils import AppModel

from ..service import PostsService, get_service
from . import router


class PostCreateRequest(AppModel):
    type: str
    price: int
    address: str
    area: float
    room_count: int
    description: str

class PostCreateResponse(AppModel):
    _id : str

@router.post("/",response_model=PostCreateResponse)
def create_post(input: PostCreateRequest,svc_post: PostsService = Depends(get_service),):
    print(input)
    done = svc_post.repository.create_post(input.dict())

    if done:
        print(done)
        return {"message":status.HTTP_200_OK}
    return {"message":status.HTTP_400_BAD_REQUEST}