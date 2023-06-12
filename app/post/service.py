from pydantic import BaseSettings

from app.config import database

from ..auth.adapters.jwt_service import JwtService
from .repository.repository import *

class AuthConfig(BaseSettings):
    JWT_ALG: str = "HS256"
    JWT_SECRET: str = "YOUR_SUPER_SECRET_STRING"
    JWT_EXP: int = 10_800


config = AuthConfig()


class PostsService:
    def __init__(self,repository: PostRepository,jwt_svc: JwtService,):
        self.repository = repository
        self.jwt_svc = jwt_svc

def get_service():
    jwt_svc = JwtService(config.JWT_ALG, config.JWT_SECRET, config.JWT_EXP)

    post_repository = PostRepository(database)
     
    svc_post = PostsService(post_repository,jwt_svc)
   
    return svc_post
