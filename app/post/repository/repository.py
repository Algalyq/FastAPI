from bson.objectid import ObjectId
from pymongo.database import Database

class PostRepository:
    def __init__(self,database:Database):
        self.database = database
    

    def create_post(self,data) -> str:
        payload = {
            "type":data["type"],
            "price":data["price"],
            "address":data["address"],
            "area":data["area"],
            "rooms_count":data["rooms_count"],
            "description": data["description"]
        }
        result = self.database["posts"].insert_one(payload)
        created_post_id = str(result.inserted_id)
        return created_post_id