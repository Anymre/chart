import datetime
import json
from datetime import datetime,timedelta

import requests
from django.shortcuts import render

# Create your views here.
from pyecharts.charts import Line

url = "http://server.anymre.top:8927/data"


def get_Date(r):
    return r["Date"]


def format(r):
    return datetime.strptime(r, "%Y-%m-%dT%H:%M:%SZ") + timedelta(hours=8)


def clean(r):
    return r.hour == 20 and r.minute == 0


def time_str(r):
    return r.strftime("%m/%d")


def perform():
    res = requests.get(url).content
    r = json.loads(res)

    f = r["Forward"]
    f.sort(key=get_Date)
    for i in f:
        i["Date"] = format(i["Date"])
        i["Now"] = format(i["Now"])

    f = [i for i in f if clean(i["Date"])]

    x = [time_str(i["Date"]) for i in f]
    y = [i["Price"] for i in f]

    l = Line()
    l.add_xaxis(x)
    l.add_yaxis("v", y)
    l.width = 768
    l.render()

from django.http import HttpResponse


def index(request):
    perform()
    return