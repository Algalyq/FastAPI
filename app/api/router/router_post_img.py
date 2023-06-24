from fastapi import Depends, UploadFile, Form
from ..service import Service, get_service
from . import router
import io
import os
import matplotlib.pyplot as plt
# from ...auth.service import Service as AuthService, get_service as auth_service

from ...auth.adapters.jwt_service import JWTData
from ...auth.router.dependencies import parse_jwt_user_data
@router.post("/file")
def upload(
    file: UploadFile,
    prompt: str = Form(...),
    duration: int = Form(...),
    svc: Service = Depends(get_service),
    jwt_data: JWTData = Depends(parse_jwt_user_data)
):
    images = svc.stability.upload_file(file.file, prompt, duration)
    output_video_path = 'output.mp4'
    # vid = svc.gcs_service.upload_video_to_gcs(images)
    urls = []
    for img in images:
        url = svc.gcs_service.upload_file(img)
        urls.append(url)
        svc.images.create_images(jwt_data.user_id,urls)
    output_file = 'result.mp4'
    video = svc.gcs_service.generate_video_from_links(urls,output_file)
    return {"msg":video}

# @router.get("/videos")
# async def get_videos(
#     svc: Service = Depends(get_service)
# ):
#     video_dir = "static/images"  # Path to your static video directory
#     video_files = []

#     for root, dirs, files in os.walk(video_dir):
#         for file in files:
#             if file.endswith(""):  # Filter for video file extensions
#                 video_files.append(os.path.join('localhost:8000',root, file))
#     # result = svc.gcs_service.list_images()
#     return {"videos": video_files}