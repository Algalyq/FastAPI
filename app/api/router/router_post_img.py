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

@router.post("/file")
def upload_file(
    file: UploadFile,
    svc: Service = Depends(get_service)
):
    content = file.file.read()
    image_stream = io.BytesIO(content)

    try:
        img = Image.open(image_stream)

        stability_api = svc.stability.stability()
        answers = stability_api.generate(
            prompt="dark background,",
            init_image=img,
            start_schedule=0.6,
            seed=123467458,
            steps=30,
            cfg_scale=8.0,
            width=512,
            height=512,
            sampler=generation.SAMPLER_K_DPMPP_2M,
            samples=1
        )

        generated_images = []
        for resp in answers:
            for artifact in resp.artifacts:
                if artifact.finish_reason == generation.FILTER:
                    warnings.warn(
                        "Your request activated the API's safety filters and could not be processed. "
                        "Please modify the prompt and try again."
                    )
                if artifact.type == generation.ARTIFACT_IMAGE:
                    img2 = Image.open(io.BytesIO(artifact.binary))
                    generated_images.append(img2)
        save_dir = "./img"  # Specify the directory where you want to save the images
        os.makedirs(save_dir, exist_ok=True)  # Create the directory if it doesn't exist

        for i, img in enumerate(generated_images):
            save_path = f"./img/generated_image_{i+1}.png"  # Adjust the file format if necessary
            with open(save_path, 'wb') as f:
                img.save(f, format='PNG')


        return {"msg": "success"}
    except Exception as e:
        return {"error": str(e)}
