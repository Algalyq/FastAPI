from datetime import datetime

from bson.objectid import ObjectId
from pymongo.database import Database

from ..utils.security import hash_password


class AuthRepository:
    def __init__(self, database: Database):
        self.database = database

    def create_user(self, user: dict):
        payload = {
            "email": user["email"],
            "password": hash_password(user["password"]),
            "created_at": datetime.utcnow(),
            "phone": None,
            "name": None,
            "city": None
        }

        self.database["users"].insert_one(payload)

    def get_user_by_id(self, user_id: str) -> dict | None:
        user = self.database["users"].find_one(
            {
                "_id": ObjectId(user_id),
            }
        )
        return user

    def get_user_by_email(self, email: str) -> dict | None:
        user = self.database["users"].find_one(
            {
                "email": email,
            }
        )
        test = self.database["users"]
        return user


        
       
    def update_user_data(self, user_id: str, data: dict):
        update_data = { }
        if data.phone:
            update_data["phone"] = data.phone
        if data.name:
            update_data["name"] = data.name
        if data.city:
            update_data["city"] = data.city
        self.database["users"].update_one({"_id": ObjectId(user_id)},{"$set":update_data})
    

