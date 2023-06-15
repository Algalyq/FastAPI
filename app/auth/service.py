from pydantic import BaseSettings

from app.config import database

from .adapters.jwt_service import JwtService
from .repository.repository import *
from .adapters.s3_service import S3Service

class AuthConfig(BaseSettings):
    JWT_ALG: str = "HS256"
    JWT_SECRET: str = "YOUR_SUPER_SECRET_STRING"
    JWT_EXP: int = 10_800

config = AuthConfig()

class Service:
    def __init__(self):
        self.repository = AuthRepository(database)
        self.favorites = FavoritesRepository(database)
        self.jwt_svc = JwtService(config.JWT_ALG, config.JWT_SECRET, config.JWT_EXP)
        self.s3_service = S3Service()


def get_service():
    svc = Service()
    return svc
