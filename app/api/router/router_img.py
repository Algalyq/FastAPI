from fastapi import Depends, UploadFile, Form
from ..service import Service, get_service
from . import router
import os


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


