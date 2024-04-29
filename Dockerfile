FROM python:3.11-slim-buster
WORKDIR /app
ADD ./requirements.txt /app/requirements.txt

RUN pip install --upgrade pip
RUN pip install -r requirements.txt

ADD . /app

EXPOSE 6008
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "6008"]