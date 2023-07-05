from .adapters.gcs_service import GCStorage
from .repository.images import ImagesRepository
from app.config import database
from .adapters.openjourney_service import OpenJourney


class Service:
    def __init__(self):
        self.gcs_service = GCStorage()
        self.images = ImagesRepository(database)
        self.openjourney = OpenJourney()

def get_service():
    svc = Service()
    return svc
