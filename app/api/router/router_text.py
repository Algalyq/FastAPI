from fastapi import Depends, UploadFile, Form,File,Body
from ..service import Service, get_service
from . import router
from app.utils import AppModel
import os
import io
from app.utils import AppModel
import wave


# body for writing reqest for user
class UserQueryRequest(AppModel):
    query: str

@router.post("/llm")
def run(  
    query: UserQueryRequest,
    svc: Service = Depends(get_service),
    ):
    
        # translate kz to ru
    kz2ru = svc.gcs_service.translate(query.query, "kk", "ru")
    
        # send query to agent llm
    response = svc.lang.model(kz2ru)

        # translate response from ru to kz
    ru2kz = svc.gcs_service.translate(response, "ru", "kk")

        # save to collections query
        # conversations = svc.repository.create_content(query.query, ru2kz)

    return {
        "msg": ru2kz,
    }



@router.get("/")
def test_run():
    return {"msg":"Wake up"}

# body for writing reqest for translate
class TranslateRequest(AppModel):
    query: str
    to: str
    fr: str

@router.post("/translater")
def translate(
    query: TranslateRequest,
    svc: Service = Depends(get_service),
):
    return svc.gcs_service.translate(query.query,query.fr,query.to)
    

