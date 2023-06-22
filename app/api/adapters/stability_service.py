
import matplotlib.pyplot as plt
from IPython.display import display
from PIL import Image
from stability_sdk import client
import stability_sdk.interfaces.gooseai.generation.generation_pb2 as generation
from typing import BinaryIO
from fastapi.middleware.cors import CORSMiddleware
import io
import os
import warnings
import cv2

class Stability:
    def __init__(self,API_KEY: str):
        self.API_KEY = API_KEY


    def upload_file(self,file: BinaryIO, prompt: str,duration: int):
        stability_api = client.StabilityInference(
        key=self.API_KEY, # API Key reference.
        verbose=True, # Print debug messages.
        engine="stable-diffusion-xl-beta-v2-2-2", # Set the engine to use for generation.
        # Available engines: stable-diffusion-v1 stable-diffusion-v1-5 stable-diffusion-512-v2-0 stable-diffusion-768-v2-0
        # stable-diffusion-512-v2-1 stable-diffusion-768-v2-1 stable-diffusion-xl-beta-v2-2-2 stable-inpainting-v1-0 stable-inpainting-512-v2-0
        )
        
        content = file.read()
        image_stream = io.BytesIO(content)

        try:
            img = Image.open(image_stream)
            
            answers = stability_api.generate(
                prompt=prompt,  
                init_image=img,
                start_schedule=0.6,
                seed=123467458,
                steps=30,
                cfg_scale=8.0,
                sampler=generation.SAMPLER_K_DPMPP_2M,
                samples=duration * 10
            )

            generated_images = []
            for resp in answers:
                for artifact in resp.artifacts:
                    if artifact.finish_reason == generation.FILTER:
                        warnings.warn(
                            "Your request activated the API's safety filters and could not be processed. "
                            "Please modify the prompt and try again."
                        )
                    if artifact.type == generation.ARTIFACT_IMAGE:
                        img2 = Image.open(io.BytesIO(artifact.binary))
                        generated_images.append(img2)
                
            output_directory = "./static/images"
            os.makedirs(output_directory, exist_ok=True)
            file_arr = []
            for i, img in enumerate(generated_images):
                save_path = f"{output_directory}/generated_image_{i+1:04d}.png"  # Adjust the file format if necessary
                img.save(save_path, format='PNG')
                file_arr.append('localhost:8000'+ save_path[1:])

            return file_arr
        except Exception as e:
            return e

    def sequence_to_video(self):
        # Convert a sequence of images into a video and delete the used images
        images_directory = "./static/images"
        output_directory = "./static/videos"
        os.makedirs(output_directory, exist_ok=True)  # Create the output directory if it doesn't exist
        fps = 12
        try:
            image_files = sorted(os.listdir(images_directory))
            if not image_files:
                raise ValueError("No images found in the specified directory.")

            # Read the first image to get the frame dimensions
            first_image_path = os.path.join(images_directory, image_files[0])
            first_image = cv2.imread(first_image_path)
            height, width, _ = first_image.shape

            # Define the video writer
            output_path = os.path.join(output_directory, "generated_video.mp4")  # Specify the output file path
            fourcc = cv2.VideoWriter_fourcc(*"mp4v")
            video_writer = cv2.VideoWriter(output_path, fourcc, fps, (width, height))

            # Write each image to the video and delete the used images
            for image_file in image_files:
                image_path = os.path.join(images_directory, image_file)
                image = cv2.imread(image_path)
                video_writer.write(image)

            video_writer.release()

            # Delete the used images
            for image_file in image_files:
                image_path = os.path.join(images_directory, image_file)
                os.remove(image_path)

            return output_path
        except Exception as e:
            return str(e)
