from bson.objectid import ObjectId
from pymongo.database import Database
from datetime import datetime

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
        images = self.database["images"].find({"post_id":post_id})
       
        if images:
            post["media"] = [image["data"] for image in images]
        else:
            post["media"] = []
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


class ImagesRepository:
    def __init__(self,database:Database):
        self.database = database

    def create_images(self,post_id,data):
        payload = {
            "post_id":post_id,
            "data": data
        }
        result = self.database["images"].insert_one(payload)
        created_post_id = str(result.inserted_id)
        return created_post_id


    def delete_images_by_post_id(self, post_id):
        result = self.database["images"].delete_many({"post_id":post_id})
        if result.deleted_count == 1:
            return True
        return False    

            
class CommentRepository:
    def __init__(self,database:Database):
        self.database = database
    

    def create_comment(self,post_id,user_id,data):
        payload = {
            "post_id": post_id,
            "created_at": datetime.utcnow(),
            "content": data,
            "author_id": user_id
        }

        result = self.database["comments"].insert_one(payload)
        return result

    def update_comment(self,comment_id,data):
        update_data = {}
        if data:
            print(data)
            update_data["content"] = data
        
        result = self.database["comments"].update_one({"_id":ObjectId(comment_id)}, {"$set":update_data})
        return result

    def delete_comment(self,comment_id):
        result = self.database["comments"].delete_one({"_id":ObjectId(comment_id)})
        if result.deleted_count == 1:
            return True
        return False   