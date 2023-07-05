
# import matplotlib.pyplot as plt
# from IPython.display import display
# from PIL import Image
# from stability_sdk import client
# import stability_sdk.interfaces.gooseai.generation.generation_pb2 as generation
# from typing import BinaryIO
# from fastapi.middleware.cors import CORSMiddleware
# import io
# import os
# import warnings
# import cv2
# import numpy as np
# import base64

# class Stability:
#     def __init__(self,API_KEY: str):
#         self.API_KEY = API_KEY


#     def upload_file(self,file: BinaryIO, prompt: str,duration: int):
#         stability_api = client.StabilityInference(
#         key=self.API_KEY, # API Key reference.
#         verbose=True, # Print debug messages.
#         engine="stable-diffusion-xl-beta-v2-2-2", # Set the engine to use for generation.
#         # Available engines: stable-diffusion-v1 stable-diffusion-v1-5 stable-diffusion-512-v2-0 stable-diffusion-768-v2-0
#         # stable-diffusion-512-v2-1 stable-diffusion-768-v2-1 stable-diffusion-xl-beta-v2-2-2 stable-inpainting-v1-0 stable-inpainting-512-v2-0
#         )
        
#         content = file.read()
#         image_stream = io.BytesIO(content)
#         img = Image.open(image_stream)
            
#         answers = stability_api.generate(
#                 prompt=prompt,  
#                 init_image=img,
#                 start_schedule=0.6,
#                 seed=123467458,
#                 steps=30,
#                 cfg_scale=8.0,
#                 sampler=generation.SAMPLER_K_DPMPP_2M,
#                 samples=duration * 10
                
#             )

#         generated_images = []
#         for resp in answers:
#             for artifact in resp.artifacts:
#                 if artifact.finish_reason == generation.FILTER:
#                     warnings.warn(
#                         "Your request activated the API's safety filters and could not be processed. "
#                         "Please modify the prompt and try again."
#                     )
#                 if artifact.type == generation.ARTIFACT_IMAGE:
#                     img2 = Image.open(io.BytesIO(artifact.binary))
#                     generated_images.append(img2)

#         generated_images_base64 = []
#         for img in generated_images:
#             buffered = io.BytesIO()
#             img.save(buffered, format="JPEG")
#             img_base64 = base64.b64encode(buffered.getvalue()).decode("utf-8")
#             generated_images_base64.append(img_base64)

#         return generated_images_base64