import requests
from fastapi import FastAPI, HTTPException
# import httpx


class J_Service:

    def __init__(self,):
        pass


    def get_random_question(self):
        url = 'https://jservice.io/api/random'

        try:
            response = requests.get(url)

            response_json = response.json()
            question_data = response_json[0] if response_json else None

            if not question_data:
                raise HTTPException(status_code=500, detail="No question was found in the response.")

            return {
                "id": question_data.get("id"),
                "question": question_data.get("question"),
                "category": question_data.get("category", {}).get("title", ""),
                "answer": question_data.get("answer"),
            }

        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))