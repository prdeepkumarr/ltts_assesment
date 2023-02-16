# Use an official Python runtime as a parent image
FROM python:3.9-slim-buster

WORKDIR /app

COPY . /app

RUN pip install  -r requirements.txt

EXPOSE 80

ENV NAME Dev

CMD ["python", "run_file.py"]
