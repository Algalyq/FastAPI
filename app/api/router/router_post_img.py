from fastapi import Depends, UploadFile
from ..service import Service, get_service
from . import router
import io
import os
import matplotlib.pyplot as plt
from PIL import Image
from stability_sdk import client
import stability_sdk.interfaces.gooseai.generation.generation_pb2 as generation
import warnings
# import cv2

@router.post("/file/")
def upload_file(
    file: UploadFile,
    prompt: str,
    duration: int,
    svc: Service = Depends(get_service)
):  

    # result = svc.stability.upload_file(file.file,prompt,duration)

    video = svc.stability.sequence_to_video()

    return {"msg": video}
