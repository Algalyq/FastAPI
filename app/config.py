from typing import Any

from pydantic import BaseSettings
from pymongo import MongoClient
from urllib.parse import quote_plus

class Config(BaseSettings):
    CORS_ORIGINS: list[str] = ["*"]
    CORS_HEADERS: list[str] = ["*"]
    CORS_METHODS: list[str] = ["GET", "POST", "PUT", "PATCH", "DELETE", "OPTIONS"]

    MONGOHOST: str
    MONGOPORT: str
    MONGOUSER: str
    MONGOPASSWORD: str
    MONGODATABASE: str
    MONGO_URL: str

# environmental variables
env = Config()
username = quote_plus(env.MONGOUSER)
password = quote_plus(env.MONGOPASSWORD)
mongo_url = "mongodb+srv://{username}:{password}@cluster0.zzr5jrn.mongodb.net/?retryWrites=true&w=majority"
print(mongo_url)
# FastAPI configurations
fastapi_config: dict[str, Any] = {
    "title": "API test",
}

if env.MONGO_URL:
    mongo_url = env.MONGO_URL
    
# MongoDB connection
client = MongoClient(mongo_url)

# MongoDB database
database = client[env.MONGODATABASE]
