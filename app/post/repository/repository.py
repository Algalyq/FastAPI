from bson.objectid import ObjectId
from pymongo.database import Database

class PostRepository:
    def __init__(self,database:Database):
        self.database = database
    

    def create_post(self,data):
        payload = {
            "type":data["type"],
            "price":data["price"],
            "address":data["address"],
            "area":data["area"],
            "room_count":data["room_count"],
            "description": data["description"]
        }

        self.database["posts"].insert_one(payload)
