from fastapi import Depends, UploadFile, Form
from ..service import Service, get_service
from . import router
# import io
# import os
# import matplotlib.pyplot as plt
# # from ...auth.service import Service as AuthService, get_service as auth_service
# import requests
# from ...auth.adapters.jwt_service import JWTData
# from ...auth.router.dependencies import parse_jwt_user_data


@router.get("/test")
def test_url(
    file: UploadFile,
    svc: Service = Depends(get_service)
):
    gcs = svc.gcs_service.upload_img(file)

    return {"msg":gcs}



# @router.post("/test")
# def upload_with_save(
#     file: UploadFile,
#     prompt: str = Form(...),
#     duration: int = Form(...),
#     svc: Service = Depends(get_service)
# ):
    
#     gcs = svc.gcs_service.upload_img(file)
#     arr_img = []
    
#     result = svc.openjourney.create_images(gcs,n=duration,prompt=prompt)
#     images_gcs = svc.gcs_service.upload_image_from_link(result[0])
#     arr_img.append(images_gcs)

#     for i in range(2):
#         result = svc.openjourney.create_images(arr_img[i], duration, prompt)
#         arr_img.append(svc.gcs_service.upload_image_from_link(result[0]))  

#     video = svc.gcs_service.generate_video_from_frames(arr_img)
#     return {
#         "result": video
#     }




# @router.post("/file")
# def upload(
#     file: UploadFile,
#     prompt: str = Form(...),
#     duration: int = Form(...),
#     svc: Service = Depends(get_service),
#     jwt_data: JWTData = Depends(parse_jwt_user_data)
# ):
#     # return images base64
#     images = svc.stability.upload_file(file.file, prompt, duration)
#     urls = []

#     for img in images:
#         url = svc.gcs_service.upload_file(img)
#         urls.append(url)
#         svc.images.create_images(jwt_data.user_id,urls)

#     output_file = 'result.mp4'
#     video = svc.gcs_service.generate_video_from_links(urls,output_file)

#     return {"msg":video}


# @router.post("/fileUp")
# def upload_to_journey(
#     file: UploadFile,
#     prompt: str = Form(...),
#     duration: int = Form(...),
#     svc: Service = Depends(get_service)
# ):
#     gcs = svc.gcs_service.upload_img(file)
#     arr_img = []
#     result = svc.openjourney.create_images(gcs,n=duration,prompt=prompt)
#     arr_img.append(result[0])
#     for i in range(1):
#         result = svc.openjourney.create_images(result[0], duration, prompt)
#         arr_img.append(result[0])  

#     output_file = 'girl.mp4'

#     links = [item[0] for item in arr_img]
#     video = svc.gcs_service.generate_video_from_links(links, output_file)
#     return {"msg":arr_img,"vid": video,"links":links}
