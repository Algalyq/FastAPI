from pydantic import BaseSettings
from app.config import database
from .adapters.here_service import HereService
from .adapters.s3_service import S3Service
from .repository.repository import PostRepository,CommentRepository,ImagesRepository

class Config(BaseSettings):
    HERE_API_KEY: str

class Service:
    def __init__(self):
        config = Config()
        self.repository = PostRepository(database)
        self.images = ImagesRepository(database)
        self.comment = CommentRepository(database)
        self.s3_service = S3Service()
        self.here_service = HereService(config.HERE_API_KEY)      

def get_service():
    svc = Service()
    return svc

