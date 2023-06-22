from .adapters.stability_service import Stability
# from pydantic import BaseSettings

from .adapters.s3_service import S3Service
# class AuthConfig(BaseSettings):
#     API_KEY: str


# config = AuthConfig()


class Service:
    def __init__(self):
        self.stability = Stability("sk-DegebbWDzledJxpIVOMmyhJClceIKHL7fKI6hxNQyjfGaT84")
        self.s3_service = S3Service()
        
def get_service():
    svc = Service()
    return svc
