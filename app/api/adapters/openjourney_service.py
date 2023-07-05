import os
import replicate
import requests


replicate_api_token = os.environ.get('REPLICATE_API_TOKEN')

class OpenJourney:

    def __init__(self):
        self.replicate = replicate.Client(replicate_api_token)
        
    def create_images(self, image_url,n,prompt):
       
        
        output = replicate.run(
            "mbentley124/openjourney-img2img:c49a9422a0d4303e6b8a8d2cf35d4d1b1fd49d32b946f6d5c74b78886b7e5dc3",
            input={
                "image": image_url,
                "prompt": prompt,
                "strength": 0.5,
                "num_images_per_prompt": 1
            }
        )
            
        return output


