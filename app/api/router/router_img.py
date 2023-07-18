from fastapi import Depends, UploadFile, Form,File,Body
from ..service import Service, get_service
from . import router
from app.utils import AppModel
import os
import io

from app.utils import AppModel
import wave


class QueryRequest(AppModel):
    query: str

@router.post("/test")
def djai2(  
    query: QueryRequest,
    svc: Service = Depends(get_service),
  
):
    # return {"msg":query.query}
    kz2ru = svc.gcs_service.translate(query.query, "kk", "ru")
    response = svc.lang.test(kz2ru)
    ru2kz = svc.gcs_service.translate(response, "ru", "kk")
    return {
        "kz2ru": kz2ru,
        "msg": ru2kz,
        "original": response
    }



@router.post("/audio")
def audio(
    audio: UploadFile = File(...),
    svc: Service = Depends(get_service)
    ):
    print(audio)
    return svc.gcs_service.upload_audio(audio)


@router.post("/testv2")
def v2test():

    # Return any desired response
    return "test"