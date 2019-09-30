import datetime
import json
import random
from datetime import datetime, timedelta

import math
import requests
from django.shortcuts import render
from django.http import HttpResponse
from pyecharts import options as opts

# Create your views here.
from django.template import loader
from pyecharts.charts import Line, EffectScatter, Line3D, Scatter3D
from pyecharts.faker import Faker
from pyecharts.globals import ThemeType

url = "http://server.anymre.top:8927/data"


def index(request, mouth, day, hour, minute):
    return HttpResponse(perform(mouth, day, hour, minute))


def get_Date(r):
    return r["Date"]


def get_Now(r):
    return r["Now"]


def format(r):
    return datetime.strptime(r, "%Y-%m-%dT%H:%M:%SZ") + timedelta(hours=8)


def clean(r, mouth, day, hour, minute):
    flag0, flag1, flag2, flag3 = True, True, True, True
    if mouth != 99:
        flag0 = r.month == mouth
    if day != 99:
        flag1 = r.day == day
    if hour != 99:
        flag2 = r.hour == hour
    if minute != 99:
        flag3 = r.minute == minute
    return flag0 and flag1 and flag2 and flag3


def time_str(r):
    return r.strftime("%m/%d %H:%M")


def time_m_d(r):
    return r.strftime("%m/%d")


def time_h_m(r):
    return r.strftime("%H:%M")


def time_h_m_int(r):
    return r.hour * 100 + r.minute

def sort_by_hour(r):
    return time_h_m_int(get_Date(r))


def chart(f):
    x = [time_str(i["Now"]) for i in f]
    y = [i["Price"] for i in f]
    l = (
        Line(init_opts=opts.InitOpts(theme=ThemeType.LIGHT, width="1366px"))
            .add_xaxis(x)
            .add_yaxis("v", y, is_connect_nones=True)
            .set_global_opts(
            title_opts=opts.TitleOpts(title="MC"),
            toolbox_opts=opts.ToolboxOpts(feature=opts.ToolBoxFeatureOpts()),
            visualmap_opts=opts.VisualMapOpts(min_=500, max_=1200),
        )
    )
    return l.render_embed()


def scatter3d_base(f) -> Scatter3D:
    f.sort(key=sort_by_hour)
    data = [
        [time_m_d(i["Now"]),time_h_m(i["Now"]), i["Price"]]
        for i in f
    ]
    c = (
        Scatter3D(init_opts=opts.InitOpts(theme=ThemeType.LIGHT, width="1366px"))
            .add("", data)
            .set_global_opts(
            visualmap_opts=opts.VisualMapOpts(min_=300,max_=1200),
            title_opts=opts.TitleOpts(title="MC"),
            toolbox_opts=opts.ToolboxOpts(feature=opts.ToolBoxFeatureOpts()),
        )
    )
    return c.render_embed()


def perform(mouth, day, hour, minute):
    res = requests.get(url).content
    r = json.loads(res)

    f = r["Forward"]
    f.sort(key=get_Date)
    f.sort(key=get_Now)

    for i in f:
        i["Date"] = format(i["Date"])
        i["Now"] = format(i["Now"])

    f = [i for i in f if clean(i["Date"], mouth, day, hour, minute)]

    # return chart(f)
    return scatter3d_base(f)
