FROM python:3

RUN apt-get update && apt-get install git && pip install django && pip install requests && pip install pyecharts && pip install mysqlclient

WORKDIR /src

COPY / .


CMD python manage.py runserver 0.0.0.0:8000