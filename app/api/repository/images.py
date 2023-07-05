# from bson.objectid import ObjectId
# from pymongo.database import Database


# class ImagesRepository:

#     def __init__(self,database:Database):
#         self.database = database

    
#     def create_images(self,user_id,data):
#         payload = {
#             "user_id": user_id,
#             "image": data
#         }

#         result = self.database["images"].insert_one(payload)
#         return result