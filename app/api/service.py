from .adapters.gcs_service import GCStorage
from app.config import database
from .adapters.lang_service import LangService
from .repository.GCS import *
from .repository.repository import *
from .adapters.j_service import * 

class Service:
    def __init__(self):
        self.gcs_service = GCStorage()
        self.lang = LangService()
        self.gcs_repository = GCSRepository(database)
        self.repository = Repository(database)
        self.j_service = J_Service()

def get_service():
    svc = Service()
    return svc
