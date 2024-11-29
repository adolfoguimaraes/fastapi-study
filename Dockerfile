FROM python:3.12-alpine

WORKDIR /code

copy ./requirements.txt /code/requirements.txt

RUN pip install --no-cache-dir --upgrade -r /code/requirements.txt

COPY app/ /code/app

RUN mkdir -p /app/logs

EXPOSE 8080

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8080"]