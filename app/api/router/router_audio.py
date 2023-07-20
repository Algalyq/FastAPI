
from fastapi import Depends, UploadFile, Form,File,Body
from ..service import Service, get_service
from . import router
from app.utils import AppModel
import os
import io


# body for transcript to audio
class Text2SpeechRequest(AppModel):
    text: str

@router.post("/audio")  # POST request endpoint at "/audio"
def text2speech(
    text: Text2SpeechRequest,  # Input parameter of type Text2SpeechRequest, likely containing the "text" to convert to speech
    svc: Service = Depends(get_service),  # Dependency injection to get the "Service" instance from the "get_service" function
):
    # Check if the text already exists in the GCS repository
    link = svc.gcs_repository.check_text_exists(text.text)
    if link:  # If the text exists in the repository
        return {"msg": link}  # Return a JSON response with the URL link to the existing audio file

    else:  # If the text does not exist in the repository
        # Convert the "text" to speech using the "text2speech" method from the "gcs_service" instance
        result = svc.gcs_service.text2speech(text.text)
        
        # Create a URL link for the newly generated audio file and store it in the GCS repository
        create_link = svc.gcs_repository.create_url(result, text.text)
        
        return {"msg": result}  # Return a JSON response with the generated audio file content
    # return {"msg":"https://storage.googleapis.com/algalyq-bucket/ec294e4ea6b6406a8b961cd9c90024ef.mp3"}