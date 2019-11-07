FROM python:3

RUN pip install django && pip install requests && pip install pyecharts && pip install mysql-connector-python && pip install mysql-connector== 8.0.18
WORKDIR /src

COPY / .


CMD python manage.py runserver 0.0.0.0:8000
