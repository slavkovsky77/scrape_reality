FROM python:3.9
COPY . /code
WORKDIR /code

RUN pip install --upgrade pip
RUN apt-get update
RUN apt-get install ffmpeg libsm6 libxext6  -y
RUN python -m pip install --upgrade pip
RUN pip install -r requirements.txt
