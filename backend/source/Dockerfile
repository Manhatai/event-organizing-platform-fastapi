FROM python:3.13

WORKDIR /code

COPY backend/source/requirements.txt /code/requirements.txt
RUN pip install --no-cache-dir --upgrade -r /code/requirements.txt

COPY backend /code/backend

CMD ["uvicorn", "backend.source.main:app", "--host", "0.0.0.0", "--port", "8000", "--ssl-keyfile", "/code/backend/source/utils/certificates/key.pem", "--ssl-certfile", "/code/backend/source/utils/certificates/cert.pem"]
