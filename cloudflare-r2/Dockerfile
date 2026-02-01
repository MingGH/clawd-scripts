FROM python:3.11-slim

RUN pip install --no-cache-dir boto3

WORKDIR /app
COPY upload_docker.py /app/

CMD ["python", "upload_docker.py"]
