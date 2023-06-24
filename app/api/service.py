from .adapters.stability_service import Stability
# from pydantic import BaseSettings
from .adapters.gcs_service import GCStorage
from .adapters.s3_service import S3Service
from .repository.images import ImagesRepository
from app.config import database



class Service:
    def __init__(self):
        self.stability = Stability("sk-tfY6EgoNOWvirdTfENMAhZp65ang99t63zxsnYgCBFwYPGzp")
        self.s3_service = S3Service()
        self.gcs_service = GCStorage()
        self.images = ImagesRepository(database)

def get_service():
    svc = Service()
    return svc
