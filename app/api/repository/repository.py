from bson.objectid import ObjectId
from pymongo.database import Database



class Repository:

    def __init__(self,database: Database):
        self.database = database



    def create_content(self,user:str,assistant: str):

        new_document = {
            'user_text': user,
            'assistant_text': assistant
        }

        # Insert the document into the collection
        result = self.database["conversations"].insert_one(new_document)

        if result.acknowledged:
            # Return the inserted document's ID
            return str(result.inserted_id)  # Convert ObjectId to a string representation
        else:
            # Return None or raise an exception to indicate failure
            return None

    def check_text_exists(self, text: str):
        # Query the collection to check if a document with the provided text exists
        existing_document = self.database["conversations"].find_one({'user_text': text})

        # Return True if a document with the text exists, False otherwise

        # Return the document's ID if it exists, otherwise return False
        return existing_document['assistant_text'] if existing_document else False