from fastapi import Depends, UploadFile, Form,File
from ..service import Service, get_service
from . import router
from app.utils import AppModel
import os
import io

import wave


@router.post("/test")
def djai2(
    svc: Service = Depends(get_service),
    query: str = Form(...)
):
    kz2ru = svc.gcs_service.translate(query, "kk", "ru")
    response = svc.lang.test(kz2ru)
    ru2kz = svc.gcs_service.translate(response, "ru", "kk")
    return {
        "kz2ru": kz2ru,
        "ru2kz": ru2kz,
        "original": response
    }




@router.post("/audio")
async def audio(audio: UploadFile = File(...),):
    audio_data = audio.file.read()
    # audio_data now contains the raw audio data in bytes

    # Convert audio_data to a WAV file
    with io.BytesIO(audio_data) as audio_stream:
        wav_file = wave.open(audio_stream, 'rb')
        # You can now process the WAV file as needed
        # For example, you can read the audio frames using wav_file.readframes() or perform any audio processing operations.

    # Return any desired response
    return {"message": "Audio received and processed successfully."}