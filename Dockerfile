FROM python:3.11

WORKDIR /code

COPY requirements.txt .

RUN pip install --upgrade -r requirements.txt

COPY . .

EXPOSE 8000

ENV IN_DOCKER_CONTAINER=true

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
