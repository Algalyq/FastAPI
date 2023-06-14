from app.config import database

# from .adapters.s3_service import S3Service
from .repository.repository import PostRepository,CommentRepository,ImagesRepository
from .adapters.s3_service import S3Service
class PostsService:
    def __init__(self):
        self.repository = PostRepository(database)
        self.images = ImagesRepository(database)
        self.comment = CommentRepository(database)
        self.s3_service = S3Service()

def get_service():
    svc_post = PostsService()
    return svc_post
