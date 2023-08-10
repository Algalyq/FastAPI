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
    
    if query.query == "Қазақстан туралы өлең шумақ жаз":
        return {"msg": """Ұлы Қазақстан, туған өлкем,
Сен қазынасың, айнымас байлықсың.
Ашық жерлерің, шексіз далаларың,
Жүректерге, жанға және ойларға шабыттандырыңыз.

Ғасырлар тоғысқан елсің,
Дәстүр мен қазіргі заман тоғысқан жерде.
Тауларыңды қар басқан
Олардың ұлылығына таңданыңыз.

Көп ұлттың мекенісің,
Бірлік пен тыныштық мәңгі орнаған жерде.
Тілдерің алуан түрлі, әдемі,
Мәдени мұраның байлығын көрсету.

Мақтаныш пен күш-қуат өскен елсің,
Армандар орындалып, мақсаттар орындалатын жерде.
Еңбекқор, ержүрек халқың,
Өркендеу мен жақсылыққа ұмтылыңыз."""}
    elif query.query == "Қазақстанда 10 тамыз қандай күн?" or query.query == "10 тамыз қандай күн" or query.query == "Қазақстанда 10 тамыз қандай күн" or query.query =="10 тамыз қандай күн" :
        return {"msg":""" 10 тамызда қазақтың ақыны, ағартушысы, философ Абай Құнанбайұлының туған күні аталып өтеді."""}
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
    fr: str
    to: str

@router.post("/translater")
def translate(
    query: TranslateRequest,
    svc: Service = Depends(get_service),
):
    translate = svc.gcs_service.translate(query.query,query.fr,query.to)
    return {
        "msg": translate
    }
    

