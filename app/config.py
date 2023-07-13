from typing import Any

from pydantic import BaseSettings
from pymongo import MongoClient
from urllib.parse import quote_plus

class Config(BaseSettings):
    CORS_ORIGINS: list[str] = ["*"]
    CORS_HEADERS: list[str] = ["*"]
    CORS_METHODS: list[str] = ["GET", "POST", "PUT", "PATCH", "DELETE", "OPTIONS"]

    MONGOHOST: str = "localhost"
    MONGOPORT: str = "27017"
    MONGOUSER: str = "algalyq"
    MONGOPASSWORD: str = "2003720An"
    MONGODATABASE: str = "fastapi"
    MONGO_URL: str = "mongodb+srv://algalyq:2003720An@cluster0.zzr5jrn.mongodb.net/?retryWrites=true&w=majority"

# environmental variables
env = Config()
username = quote_plus(env.MONGOUSER)
password = quote_plus(env.MONGOPASSWORD)
mongo_url = f"mongodb+srv://{username}:{password}@cluster0.zzr5jrn.mongodb.net/?retryWrites=true&w=majority"

# FastAPI configurations
fastapi_config: dict[str, Any] = {
    "title": "API test",
}

    
# MongoDB connection
client = MongoClient(mongo_url)

# MongoDB database
database = client[env.MONGODATABASE]

