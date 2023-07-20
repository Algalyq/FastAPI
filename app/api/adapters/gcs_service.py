from google.cloud import storage,translate,speech
import os 
import base64   
from typing import BinaryIO
import uuid
import io
from fastapi import UploadFile
import numpy as np
import imageio
import requests
import urllib.request
from moviepy.editor import ImageSequenceClip
import tempfile
from PIL import Image
from googletrans import Translator
from google.cloud.speech_v1 import types

from fastapi.encoders import jsonable_encoder

os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = r'cert/gcs-key.json'


SPEECH_REGION=os.getenv("SPEECH_REGION")
SPEECH_KEY=os.getenv("SPEECH_KEY")



class GCStorage:

    def __init__(self):
        self.storage_client = storage.Client()
        self.bucket_name = 'algalyq'


    def text2speech(self, query: str):
        url = f"https://{SPEECH_REGION}.tts.speech.microsoft.com/cognitiveservices/v1"
        headers = {
            "Ocp-Apim-Subscription-Key": SPEECH_KEY,
            "Content-Type": "application/ssml+xml",
            "X-Microsoft-OutputFormat": "audio-16khz-128kbitrate-mono-mp3"
        }

        data = f'''<speak version='1.0' xml:lang='kk-KZ'><voice xml:lang='kk-KZ' xml:gender='Male' name='kk-KZ-DauletNeural'>{query}</voice></speak>'''

        data_utf8 = data.encode('utf-8')
        response = requests.post(url, headers=headers, data=data_utf8)
        if response.status_code == 200:
            # Upload to Google Cloud Storage
            unique_id = uuid.uuid4().hex
            file_name = f"{unique_id}.mp3"

            storage_client = storage.Client()
            bucket = self.storage_client.bucket(self.bucket_name)
            blob = bucket.blob(file_name)

            # Use io.BytesIO to work with bytes in-memory
            audio_bytes = io.BytesIO(response.content)
            blob.upload_from_file(audio_bytes, content_type="audio/mpeg")
            print(f"Audio file uploaded to Google Cloud Storage: gs://{self.bucket_name}/{file_name}")

        else:
            print(f"Error: {response.status_code} - {response.text}")

        return f"https://storage.googleapis.com/{self.bucket_name}/{file_name}"



    def upload_audio(self,file: UploadFile):
        # Create a client to interact with Google Cloud Storage
        bucket = self.storage_client.get_bucket(self.bucket_name)
       
        # Set the destination file name in the bucket
        destination_blob_name = file.filename

        # Upload the file to Google Cloud Storage
        blob = bucket.blob(destination_blob_name)
        blob.upload_from_file(file.file, content_type="audio/wav")

        # Close the file after upload
        file.file.close()

        # Return the URL of the uploaded file
        return f"https://storage.googleapis.com/{self.bucket_name}/{destination_blob_name}"
            


    def export_transcript_to_storage_beta(
        input_storage_uri: str = "",
        output_storage_uri: str= "",
        encoding: str = speech.RecognitionConfig.AudioEncoding.LINEAR16,
        sample_rate_hertz: int = 8000,
        language_code: str = "kk",
        object_name: str = "algalyq/trans/",
    ):
        # input_uri URI for audio file in Cloud Storage, e.g. gs://[BUCKET]/[FILE]
        audio = speech.RecognitionAudio(uri=input_storage_uri)

        # Pass in the URI of the Cloud Storage bucket to hold the transcription
        output_config = speech.TranscriptOutputConfig(gcs_uri=output_storage_uri)

        # Speech configuration object
        config = speech.RecognitionConfig(
            encoding=encoding,
            sample_rate_hertz=sample_rate_hertz,
            language_code=language_code,
        )

        # Compose the long-running request
        request = speech.LongRunningRecognizeRequest(
            audio=audio, config=config, output_config=output_config
        )

        # create the speech client
        speech_client = speech.SpeechClient()

        # create the storage client
        storage_client = storage.Client()

        # run the recognizer to export transcript
        operation = speech_client.long_running_recognize(request=request)

        print("Waiting for operation to complete...")
        operation.result(timeout=90)

        # get bucket with name
        bucket = self.storage_client.get_bucket(self.bucket_name)

        # get blob from bucket
        blob = bucket.get_blob(object_name)

        # get content as bytes
        results_bytes = blob.download_as_bytes()

        # get transcript exported in storage bucket
        storage_transcript = types.LongRunningRecognizeResponse.from_json(
            results_bytes, ignore_unknown_fields=True
        )

        # Each result is for a consecutive portion of the audio. Iterate through
        # them to get the transcripts for the entire audio file.
        for result in storage_transcript.results:
            # The first alternative is the most likely one for this portion.
            print(f"Transcript: {result.alternatives[0].transcript}")
            print(f"Confidence: {result.alternatives[0].confidence}")

        # [END speech_transcribe_with_speech_to_storage_beta]
        return storage_transcript.results


    def translate(self, text: str,fr: str,to: str):
        client = translate.TranslationServiceClient()
        project_id = "nurai-390616"
        location = "global"

        parent = f"projects/{project_id}/locations/{location}"

        # Translate text from English to French
        # Detail on supported types can be found here:
        # https://cloud.google.com/translate/docs/supported-formats
        response = client.translate_text(
            request={
                "parent": parent,
                "contents": [text],
                "mime_type": "text/plain",  # mime types: text/plain, text/html
                "source_language_code": fr,
                "target_language_code": to,
            }
        )
        result = ""
        # Display the translation for each input text provided
        for translation in response.translations:
            result += translation.translated_text

        return result


    def upload_img(self, image):
        bucket = self.storage_client.get_bucket(self.bucket_name)
        file_path = "images/" + image.filename
        blob = bucket.blob(file_path)
        blob.upload_from_file(image.file, content_type='image/jpeg')
        return blob.public_url
        
    def upload_image_from_link(self,links):
        bucket = self.storage_client.get_bucket(self.bucket_name)
        uploaded_image_links = []

        for link in links:
            # Fetch the image from the link
            response = urllib.request.urlopen(link)
            image_data = response.read()

            # Generate a unique filename for the image
            gcs_filename = "images/" + str(uuid.uuid4())

            # Create a new blob with the desired filename
            blob = bucket.blob(gcs_filename)

            # Upload the image data to the blob
            blob.upload_from_string(image_data)

            # Generate and store the public URL of the uploaded image
            uploaded_image_url = f"https://storage.googleapis.com/{self.bucket_name}/{gcs_filename}"
            uploaded_image_links.append(uploaded_image_url)

        return uploaded_image_links

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
        clip = ImageSequenceClip(frames, fps=12)

        # Set up the temporary file for saving the video
        output_filename = tempfile.mktemp(suffix=".mp4")
        
        # Save the video to the temporary file
        clip.write_videofile(output_filename, codec="libx264")

        # Upload the video file to Google Cloud Storage
        bucket = self.storage_client.get_bucket(self.bucket_name)
        blob = bucket.blob(output_filename[5:])
        blob.upload_from_filename(output_filename)

        return f"https://storage.googleapis.com/{self.bucket_name}/{output_filename[5:]}"
