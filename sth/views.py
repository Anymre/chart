import datetime
import json
from datetime import datetime, timedelta

import requests
from django.shortcuts import render

# Create your views here.
from django.template import loader
from pyecharts.charts import Line

url = "http://server.anymre.top:8927/data"


def get_Date(r):
    return r["Date"]


def format(r):
    return datetime.strptime(r, "%Y-%m-%dT%H:%M:%SZ") + timedelta(hours=8)


def clean(r, mouth, day, hour, minute):
    flag = True
    if mouth != 99:
        flag = r.month == mouth
    if day != 99:
        flag = r.day == day
    if hour != 99:
        flag = r.hour == hour
    if minute != 99:
        flag = r.minute == minute
    return flag


def time_str(r):
    return r.strftime("%m/%d")


def perform(mouth, day, hour, minute):
    res = requests.get(url).content
    r = json.loads(res)

    f = r["Forward"]
    f.sort(key=get_Date)
    for i in f:
        i["Date"] = format(i["Date"])
        i["Now"] = format(i["Now"])

    f = [i for i in f if clean(i["Date"], mouth, day, hour, minute)]

    x = [time_str(i["Date"]) for i in f]
    y = [i["Price"] for i in f]

    l = Line()
    l.add_xaxis(x)
    l.add_yaxis("v", y)
    l.width = 768
    return l.render_embed()


from django.http import HttpResponse


def index(request, mouth, day, hour, minute):
    return HttpResponse(perform(mouth, day, hour, minute))
