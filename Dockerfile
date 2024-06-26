FROM python:3.9
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
RUN apt-get update
WORKDIR /code
COPY . /code/
RUN pip install --upgrade pip && pip install -r requirements.txt
COPY . /code/
