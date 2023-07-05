from google.cloud import storage 
import os 
import base64   
from typing import BinaryIO
import uuid
import io
import numpy as np
import imageio
import requests
import urllib.request

from moviepy.editor import ImageSequenceClip
import tempfile
from PIL import Image
os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = r'cert/gcs-key.json'

class GCStorage:

    def __init__(self):
        self.storage_client = storage.Client()
        self.bucket_name = 'algalyq-bucket'


    def upload_img(self, image):
        bucket = self.storage_client.get_bucket(self.bucket_name)
        file_path = "images/" + image.filename
        blob = bucket.blob(file_path)
        blob.upload_from_file(image.file, content_type='image/jpeg')
        return blob.public_url

    def upload_image_from_link(self,link):
        # Fetch the image from the link
        response = urllib.request.urlopen(link)
        image_data = response.read()
        bucket = self.storage_client.get_bucket(self.bucket_name)
        gcs_filename = "images/" + str(uuid.uuid4())   
        # Create a new blob with the desired filename
        blob = bucket.blob(gcs_filename)
        
        # Upload the image data to the blob
        blob.upload_from_string(image_data)

        # Generate and return the public URL of the uploaded image
        return f"https://storage.googleapis.com/{self.bucket_name}/{gcs_filename}"

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
        writer = imageio.get_writer(output_file, fps=4)

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
            

    def generate_video_from_frames(self, links):
        frames = []
        first_frame = None

        for link in links:
            # Fetch the image from the link
            response = urllib.request.urlopen(link)
            img = Image.open(response)
            img_array = np.array(img)

            # Resize the image if it doesn't match the size of the first frame
            if first_frame is None:
                first_frame = img
            elif img.size != first_frame.size:
                img = img.resize(first_frame.size)
                img_array = np.array(img)

            frames.append(img_array)

        # Create the video clip from frames using moviepy
        clip = ImageSequenceClip(frames, fps=4)

        # Set up the temporary file for saving the video
        output_filename = tempfile.mktemp(suffix=".mp4")
        
        # Save the video to the temporary file
        clip.write_videofile(output_filename, codec="libx264")

        # Upload the video file to Google Cloud Storage
        bucket = self.storage_client.get_bucket(self.bucket_name)
        blob = bucket.blob(output_filename[5:])
        blob.upload_from_filename(output_filename)

        return f"https://storage.googleapis.com/{self.bucket_name}/{output_filename[5:]}"
