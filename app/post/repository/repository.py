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


    def get_post_by_id(self, post_id):
        post = self.database["posts"].find_one({"_id": ObjectId(post_id)})
        return post    

    def update_post_data(self,post_id,data):
        update_data = {}
        if getattr(data, 'type', None):
            update_data['type'] = data.type
        if getattr(data, 'price', None):
            update_data['price'] = data.price
        if getattr(data, 'address', None):
            update_data['address'] = data.address
        if getattr(data, 'area', None):
            update_data['area'] = data.area
        if getattr(data, 'rooms_count', None):
            update_data['rooms_count'] = data.rooms_count
        if getattr(data, 'description', None):
            update_data['description'] = data.description

        self.database["posts"].update_one({"_id": ObjectId(post_id)}, {"$set": update_data})

        return True
    
    def delete_post_by_id(self, post_id):
        result = self.database["posts"].delete_one({"_id": ObjectId(post_id)})
        if result.deleted_count == 1:
            return True
        return False    