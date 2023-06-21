
import matplotlib.pyplot as plt
from IPython.display import display
from PIL import Image
from stability_sdk import client
import stability_sdk.interfaces.gooseai.generation.generation_pb2 as generation

from fastapi.middleware.cors import CORSMiddleware


class Stability:
    def __init__(self,API_KEY: str):
        self.API_KEY = API_KEY


    def stability(self):
        stability_api = client.StabilityInference(
        key=self.API_KEY, # API Key reference.
        verbose=True, # Print debug messages.
        engine="stable-diffusion-xl-beta-v2-2-2", # Set the engine to use for generation.
        # Available engines: stable-diffusion-v1 stable-diffusion-v1-5 stable-diffusion-512-v2-0 stable-diffusion-768-v2-0
        # stable-diffusion-512-v2-1 stable-diffusion-768-v2-1 stable-diffusion-xl-beta-v2-2-2 stable-inpainting-v1-0 stable-inpainting-512-v2-0
        )
        return stability_api