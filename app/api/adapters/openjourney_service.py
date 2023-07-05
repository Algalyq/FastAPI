# import os
# from dotenv import dotenv_values
# import replicate
# import requests

# env_vars = dotenv_values('.env')
# replicate_api_token = env_vars.get('REPLICATE_API_TOKEN')
# os.environ['REPLICATE_API_TOKEN'] = replicate_api_token
# class OpenJourney:
#     def __init__(self):
#         self.replicate = replicate.Client(replicate_api_token)
        
#     def create_images(self, image_url,n,prompt):
#         image = image_url
        
#         output = replicate.run(
#             "mbentley124/openjourney-img2img:c49a9422a0d4303e6b8a8d2cf35d4d1b1fd49d32b946f6d5c74b78886b7e5dc3",
#             input={
#                 "image": image,
#                 "prompt": prompt,
#                 "strength": 0.5,
#                 "num_images_per_prompt": 1
#             }
#         )
            
#         return output


