# syntax=docker/dockerfile:1
FROM python:3.10
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
EXPOSE 8000
WORKDIR /code
COPY requirements.txt /code
RUN pip3 install -r requirements.txt --no-cache-dir
COPY . /code
RUN ["chmod", "+x", "/code/docker-entrypoint.sh"]
