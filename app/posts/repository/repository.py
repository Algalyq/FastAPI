from bson.objectid import ObjectId
from pymongo.database import Database
from datetime import datetime

from fastapi import Depends
# from ..service import Service,get_service
from geopy.distance import distance
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
            "description": data["description"],
            "approve": False
        }
        result = self.database["posts"].insert_one(payload)
        created_post_id = str(result.inserted_id)
        return created_post_id

    def get_post_by_id(self, post_id):
        post = self.database["posts"].find_one({"_id": ObjectId(post_id)})
        images = self.database["images"].find({"post_id":post_id})
        merged_list = []
        for image in images:
            merged_list.extend(image["data"])
        if images:
            post["media"] = merged_list
        else:
            post["media"] = []
        return post

    def get_post_approved(self):
        posts = list(self.database["posts"].find({}))
        objects = []
        for item in posts:
            if item["approve"] == True:
                objects.append({
                "_id": str(item["_id"]),
                "type": item["type"],
                "price": item["price"],
                "address": item["address"],
                "area": item["area"],
                "rooms_count": item["rooms_count"],
                "approve":item["approve"]
            })
        return objects
    

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

    def search_pagination(self,query: dict,offset: int, limit: int):
        total = self.database["posts"].count_documents(query)
        posts = self.database["posts"].find(query)
        objects = []
        
        
        if latitude is not None and longitude is not None and radius is not None:
            posts = self.filter_by_location(posts, latitude, longitude, radius)

        posts = posts.sort("_id",-1).skip(offset).limit(limit)
       
        for item in posts:
            objects.append({
                "_id": str(item["_id"]),
                "type": item["type"],
                "price": item["price"],
                "address": item["address"],
                "area": item["area"],
                "rooms_count": item["rooms_count"],
            })
        result = {
            "total": total,
            "objects": objects
        }
        return result

    # def filter_by_location(self, posts, latitude, longitude, radius):
    #     filtered_posts = []
    #     center = (latitude, longitude)
    #     svc: Service = Depends(get_service)
        
    #     for item in posts:
            
    #         location = svc.here_service.get_coordinates(item["address"])
    #         if location is not None:
    #             post_location = (location.latitude, location.longitude)
    #             dist = distance(center, post_location)
    #             if dist <= radius:
    #                 filtered_posts.append(item)

    #     return filtered_posts

    def get_post_to_approve(self,offset: int, limit: int):
        posts = list(self.database["posts"].find().sort("_id",-1).skip(offset).limit(limit))
        objects = []
        for item in posts:
            if item["approve"] != True and item["approve"] != None:
                objects.append({
                "_id": str(item["_id"]),
                "type": item["type"],
                "price": item["price"],
                "address": item["address"],
                "area": item["area"],
                "rooms_count": item["rooms_count"]
            })
        return objects


    def update_to_approve(self,id: str):
        update_data = {"approve":True}
        posts = self.database["posts"].update_one({"_id":ObjectId(id)},{"$set":update_data})
        return posts

    def update_to_decline(self,id: str):
        update_data = {"approve":None}
        posts = self.database["posts"].update_one({"_id":ObjectId(id)},{"$set":update_data})
        return posts


class ImagesRepository:
    def __init__(self,database:Database):
        self.database = database

    def create_images(self,post_id,data):
        payload = {
            "post_id":post_id,
            "data": [data]
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
    
    def get_comments(self,post_id):
        result = self.database["comments"].find({"post_id":post_id})

        comments = []
        for item in result:
            comments.append({
                "_id": str(item["_id"]),
                "content": item["content"],
                "created_at":item["created_at"],
                "author_id":item["author_id"]
            })

        if comments:
            return comments

        return {}