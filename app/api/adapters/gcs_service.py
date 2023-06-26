from google.cloud import storage 
import os 
import cv2
import base64   
import uuid
import io
import os
import warnings
import cv2
import numpy as np
import imageio
import requests
from PIL import Image
os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = r'cert/gcs-key.json'

class GCStorage:

    def __init__(self):
        self.storage_client = storage.Client()
        self.bucket_name = 'algalyq-bucket'


    def upload_file(self,base64_image: list):
        bucket = self.storage_client.get_bucket(self.bucket_name)
        image_data = base64_image

    # Convert the base64 data to bytes
        image_bytes = base64.b64decode(image_data)
        filename = str(uuid.uuid4())
        file_path = "algalyq/" + filename
        blob = bucket.blob(file_path)
        blob.upload_from_string(image_bytes, content_type='image/jpeg')

        # blob.upload_from_file(file.file,content_type='image/png')
        return f'https://storage.googleapis.com/{self.bucket_name}/{file_path}'
    

    def generate_video_from_links(self,image_links, output_file):
            # Initialize an empty list to store the downloaded images
        images = []

        # Download and append each image to the list
        for link in image_links:
            response = requests.get(link)
            image = Image.open(io.BytesIO(response.content))
            images.append(image)

        # Check if any images were downloaded
        if len(images) == 0:
            print("No images were downloaded.")
            return

  
    # Create a writer object to save the video frames directly to Google Cloud Storage
        writer = imageio.get_writer(output_file, fps=12)

        # Write each image to the video
        for image in images:
            # Convert the PIL image to a numpy array
            frame = np.array(image)

            # Append the frame to the video
            writer.append_data(frame)

        # Close the writer to save the video
        writer.close()

        bucket = self.storage_client.get_bucket(self.bucket_name)
        
        blob = bucket.blob(output_file)
        blob.upload_from_filename(output_file)


        return f"https://storage.googleapis.com/{self.bucket_name}/{output_file}"
            
