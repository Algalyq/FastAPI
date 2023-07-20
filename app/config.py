from typing import Any

from pydantic import BaseSettings
from pymongo import MongoClient
from urllib.parse import quote_plus

class Config(BaseSettings):
    CORS_ORIGINS: list[str] = ["http://localhost:3000",]
    CORS_HEADERS: list[str] = ["*"]
    CORS_METHODS: list[str] = ["*"]

    MONGOHOST: str = "localhost"
    MONGOPORT: str = "27017"
    MONGOUSER: str = "algalyq"
    MONGOPASSWORD: str = "qijpoc-6mirHe-zybsan"
    MONGODATABASE: str = "fastapi"
    MONGO_URL: str = "mongodb+srv://algalyq:qijpoc-6mirHe-zybsan@cluster0.zzr5jrn.mongodb.net/?retryWrites=true&w=majority"

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

