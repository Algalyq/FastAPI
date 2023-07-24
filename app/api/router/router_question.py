from fastapi import Depends, UploadFile, Form,File,Body,HTTPException
from ..service import Service, get_service
from . import router
from app.utils import AppModel

@router.get('/question')
def question_generate(
    svc: Service = Depends(get_service)
):
    question = svc.j_service.get_random_question()

    translateToRu = svc.gcs_service.translate(question["question"],"en","ru")


    translate2Kz = svc.gcs_service.translate(translateToRu,"ru","kk")
    return {"msg": translate2Kz}

