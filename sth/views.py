import datetime
import json
from datetime import datetime, timedelta

import requests
from django.http import HttpResponse
from pyecharts import options as opts
# Create your views here.
from pyecharts.charts import Line, Scatter3D
from pyecharts.globals import ThemeType

from sth.models import Forward,Back


def index(request, mouth, day, type):
    return HttpResponse(perform(mouth, day, type))


def clean(r, mouth, day, hour, minute):
    flag0, flag1, flag2, flag3 = True, True, True, True
    r = r.date
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
    data = [
        [time_m_d(i.now), time_h_m(i.now), i.price]
        for i in f
    ]
    name = ["d", "h", "v"]
    c = (
        Scatter3D(init_opts=opts.InitOpts(theme=ThemeType.LIGHT, width="1366px"))
            .add("", data, )
            .set_global_opts(
            visualmap_opts=opts.VisualMapOpts(min_=300, max_=1200),
            title_opts=opts.TitleOpts(title="MC"),
            toolbox_opts=opts.ToolboxOpts(feature=opts.ToolBoxFeatureOpts()),
        )
    )
    return c.render_embed()


def perform(mouth, day, type):
    result=[]
    if (type == 0):
        forwards = Forward.objects.filter(date__day=day, date__month=mouth).order_by("now")
        result = [i for i in forwards if clean(i, mouth, day, 99, 0)]
    if (type == 1):
        back = Back.objects.filter(date__day=day, date__month=mouth).order_by("now")
        result = [i for i in back if clean(i, mouth, day, 99, 0)]

    return scatter3d_base(result)
