
import requests
import os

class HereAPI:
    def __init__(self):
        pass

    def get_coordinate(self,path: str):

        url = "https://geocode.search.hereapi.com/v1/geocode"
        api_key = os.getenv("API_KEY")
        query = "Invalidenstr 117 Berlin"

        params = {
            "q": query,
            "apiKey": api_key
        }

        response = requests.post(url, params=params)

        if response.status_code == 200:
            # Request was successful
            data = response.json()
            # Process the response data
            return data["postion"]
        else:
            # Request failed
            return None
