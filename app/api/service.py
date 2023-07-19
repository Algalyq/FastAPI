from .adapters.gcs_service import GCStorage
from app.config import database
from .adapters.lang_service import LangService
from .adapters.azure_service import Azure_Service
class Service:
    def __init__(self):
        self.gcs_service = GCStorage()
        self.lang = LangService()
        self.azure = Azure_Service()

def get_service():
    svc = Service()
    return svc
