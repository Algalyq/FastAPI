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
            "phone": "",
            "name": "",
            "city": "",
            "avatar_url":"",
            "role":"user"
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
    
    def post_avatar_user(self,user_id: str,path: str):
        update_data = {}
        if path:
            update_data["avatar_url"] = path
        result = self.database["users"].update_one({"_id": ObjectId(user_id)},{"$set":update_data})
        return result

    def delete_avatar_user(self, user_id: str):
        filter = {"_id": ObjectId(user_id)}
        update = {"$unset": {"avatar_url": ""}}
        result = self.database["users"].update_one(filter, update)


        if result.modified_count > 0:
            return True
        
        return False


class FavoritesRepository:
    def __init__(self,database:Database):
        self.database = database


    def create_fav(self,user_id: str, data: dict):
        payload = {
            "user_id": user_id,
            "address": data
        }
        self.database["favorites"].insert_one(payload)
        return True


    def get_favorites(self,user_id: str):
        result = self.database["favorites"].find({"user_id":user_id})

        favorites = []
        for item in result:
            favorites.append({
                "_id": str(item["_id"]),
                "address": item["address"]
            })

        if favorites:
            return favorites

        return {}

    def delete_favorites(self,id: str):
        result = self.database["favorites"].delete_one({"_id":ObjectId(id)})
        if result.deleted_count == 1:
            return True
        return False