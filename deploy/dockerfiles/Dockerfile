FROM python:3.11 as requirements-stage

WORKDIR /tmp
RUN pip install poetry==1.5.0
COPY ./pyproject.toml ./poetry.lock* /tmp/
RUN poetry export -f requirements.txt --output requirements.txt --without-hashes --with=dev


FROM python:3.11

WORKDIR /code
COPY --from=requirements-stage /tmp/requirements.txt .
RUN apt update && apt install -y libsm6 libxext6 ffmpeg libfontconfig1 libxrender1 libgl1-mesa-glx

RUN pip install --no-cache-dir --upgrade -r ./requirements.txt && pip install geopy && pip install opencv-python

COPY . .

ENTRYPOINT ["sh", "./scripts/launch.sh"]