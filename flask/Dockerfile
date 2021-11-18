FROM python:3.8.12-buster
LABEL maintainer="Tanaka Kazuki"
LABEL discription = "OnlineJudge By Flask"

WORKDIR /app

RUN mkdir templates
COPY ./templates/ /app/templates
COPY ./dbaccess.py /app
COPY ./judge.py /app
COPY ./app.py /app

RUN pip install flask psycopg2-binary



CMD ["python","app.py"]












