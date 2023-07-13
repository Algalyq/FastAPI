from .adapters.gcs_service import GCStorage
from app.config import database
from .adapters.lang_service import LangService

class Service:
    def __init__(self):
        self.gcs_service = GCStorage()
        self.lang = LangService()

def get_service():
    svc = Service()
    return svc
