# encoding: utf-8

"""
@version:
@author: liriqiang
@file: rrdgraph.py
@time: 16-6-23 下午6:23
"""

import urllib
from opsplatform.api import *
from monitor.monitor_api import *
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from consts import RRD_CFS, GRAPH_TYPE_KEY, GRAPH_TYPE_HOST, ENDPOINT_DELIMITER, COUNTER_DELIMITER
from monitor.models import *
from rrdgraph import merge_list
from rrdgraph import graph_query
from graph_url import generate_graph_urls


@login_required(login_url='/login')
def index(request):
    return render_to_response('monitor/monitor.html', locals(), RequestContext(request))


def api_endpoints(request):
    ret = {
        "ok": False,
        "msg": "",
        "data": [],
    }

    q = request.GET.get("q") or ""
    raw_tag = request.GET.get("tags") or ""
    tags = raw_tag and [x.strip() for x in raw_tag.split(",")] or []
    limit = int(request.GET.get("limit") or 100)

    if not q and not tags:
        ret["msg"] = "no query params given"
        return JsonResponse(ret)

    endpoints = []

    if tags and q:
        endpoint_ids = TagEndpoint.get_endpoint_ids(tags, limit=limit) or []
        endpoints = Endpoint.search_in_ids(q.split(), endpoint_ids)
    elif tags:
        endpoint_ids = TagEndpoint.get_endpoint_ids(tags, limit=limit) or []
        endpoints = Endpoint.gets(endpoint_ids)
    else:
        endpoints = Endpoint.search(q.split(), limit=limit)

    endpoints_str = [x.endpoint for x in endpoints]
    endpoints_str.sort()
    ret['data'] = endpoints_str
    ret['ok'] = True
    return JsonResponse(ret)


def api_counters(request):
    ret = {
        "ok": False,
        "msg": "",
        "data": [],
    }
    endpoints = request.POST.get("endpoints") or ""
    endpoints = endpoints and json.loads(endpoints)
    q = request.POST.get("q") or ""
    print q
    limit = int(request.POST.get("limit") or 100)

    if not (endpoints or q):
        ret['msg'] = "no endpoints or counter given"
        return JsonResponse(ret)

    endpoint_objs = Endpoint.gets_by_endpoint(endpoints)
    endpoint_ids = [x.id for x in endpoint_objs]
    if not endpoint_ids:
        ret['msg'] = "no endpoints in graph"
        return JsonResponse(ret)

    if q:
        qs = q.split()
        ecs = EndpointCounter.search_in_endpoint_ids(qs, endpoint_ids, limit=limit)
    else:
        ecs = EndpointCounter.gets_by_endpoint_ids(endpoint_ids, limit=limit)

    if not ecs:
        ret["msg"] = "no counters in graph"
        return JsonResponse(ret)

    counters_map = {}
    for x in ecs:
        counters_map[x.counter] = [x.counter, x.type_, x.step]
    sorted_counters = sorted(counters_map.keys())
    sorted_values = [counters_map[x] for x in sorted_counters]

    ret['data'] = sorted_values
    ret['ok'] = True

    return JsonResponse(ret)


@login_required(login_url='/login')
def chart(request):
    endpoints = request.POST.getlist("endpoints[]") or []
    counters = request.POST.getlist("counters[]") or []
    graph_type = request.POST.get("graph_type") or GRAPH_TYPE_HOST
    es = endpoints and ENDPOINT_DELIMITER.join(sorted(endpoints)) or ""
    cs = counters and COUNTER_DELIMITER.join(sorted(counters)) or ""
    ck = hashlib.md5("%s:%s" % (es.encode("utf8"), cs.encode("utf8"))).hexdigest()
    tmpgraph, create = TmpGraph.objects.get_or_create(endpoints=es,
                                                      counters=cs,
                                                      ck=ck,
                                                      time=datetime.datetime.now())
    id_ = tmpgraph.id
    ret = {
            "ok": False,
            "id": id_,
            "params": {
                "graph_type": graph_type,
            },
    }
    if id_:
        ret['ok'] = True
    return JsonResponse(ret)


@login_required(login_url='/login')
def chart_big(request):
    now = int(time.time())
    id = request.GET.get("id") or ""
    cols = request.GET.get("cols") or "2"
    try:
        cols = int(cols)
    except:
        cols = 2
    if cols <= 0:
        cols = 2
    if cols >= 6:
        cols = 6
    legend = request.GET.get("legend") or "off"
    cf = (request.GET.get("cf") or "AVERAGE").upper() # MAX, MIN, AVGRAGE, LAST
    sum = request.GET.get("sum") or "off"
    sumonly = request.GET.get("sumonly") or "off" #是否只显示求和
    graph_type = request.GET.get("graph_type") or GRAPH_TYPE_HOST
    nav_header = request.GET.get("nav_header") or "on"
    start = int(request.GET.get("start") or -3600)
    if start < 0:
        start = now + start
    end = int(request.GET.get("end") or 0)
    if end <= 0:
        end = now + end
    end = end - 60
    limit = int(request.GET.get("limit") or 0)
    page = int(request.GET.get("page") or 0)
    return render_to_response("monitor/chart/big_ng.html", locals(), RequestContext(request))


def multi_endpoints_chart_data(request):
    now = int(time.time())
    id = request.GET.get("id") or ""
    cols = request.GET.get("cols") or "2"
    try:
        cols = int(cols)
    except:
        cols = 2
    if cols <= 0:
        cols = 2
    if cols >= 6:
        cols = 6
    legend = request.GET.get("legend") or "off"
    cf = (request.GET.get("cf") or "AVERAGE").upper() # MAX, MIN, AVGRAGE, LAST
    sum = request.GET.get("sum") or "off"
    sumonly = request.GET.get("sumonly") or "off" #是否只显示求和
    graph_type = request.GET.get("graph_type") or GRAPH_TYPE_HOST
    nav_header = request.GET.get("nav_header") or "on"
    start = int(request.GET.get("start") or -3600)
    if start < 0:
        start = now + start
    end = int(request.GET.get("end") or 0)
    if end <= 0:
        end = now + end
    end = end - 60
    limit = int(request.GET.get("limit") or 0)
    page = int(request.GET.get("page") or 0)

    if not id:
        return HttpResponse("no graph id given")
    try:
        tmp_graph = TmpGraph.objects.get(id=id)
    except:
        tmp_graph = None
    if not tmp_graph:
        return HttpResponse("no graph which id is %s" %id)
    counters = tmp_graph.counters.split(COUNTER_DELIMITER)
    if not counters:
        return HttpResponse("no counters of %s" %id)
    counters = sorted(set(counters))

    endpoints = tmp_graph.endpoints.split(ENDPOINT_DELIMITER)
    if not endpoints:
        return HttpResponse("no endpoints of %s" % (id,))
    endpoints = sorted(set(endpoints))
    ret = {
            "units": "",
            "title": "",
            "series": []
    }
    ret['title'] = counters[0]
    c = counters[0]
    endpoint_counters = []
    for e in endpoints:
        endpoint_counters.append({
            "endpoint": e,
            "counter": c,
        })

    query_result = graph_query(endpoint_counters, cf, start, end)
    series = []
    for i in range(0, len(query_result)):
        x = query_result[i]
        try:
            xv = [(v["timestamp"]*1000, v["value"]) for v in x["Values"]]
            serie = {
                    "data": xv,
                    "name": query_result[i]["endpoint"],
                    "cf": cf,
                    "endpoint": query_result[i]["endpoint"],
                    "counter": query_result[i]["counter"],
            }
            series.append(serie)
        except:
            pass
    sum_serie = {
            "data": [],
            "name": "sum",
            "cf": cf,
            "endpoint": "sum",
            "counter": c,
    }
    if sum == "on" or sumonly == "on":
        sum = []
        tmp_ts = []
        max_size = 0
        for serie in series:
            serie_vs = [x[1] for x in serie["data"]]
            if len(serie_vs) > max_size:
                max_size = len(serie_vs)
                tmp_ts = [x[0] for x in serie["data"]]
            sum = merge_list(sum, serie_vs)
        sum_serie_data = []
        for i in range(0, max_size):
            sum_serie_data.append((tmp_ts[i], sum[i]))
        sum_serie['data'] = sum_serie_data

        series.append(sum_serie)

    if sumonly == "on":
        ret['series'] = [sum_serie, ]
    else:
        ret['series'] = series
    return JsonResponse(ret)


def multi_counters_chart_data(request):
    now = int(time.time())
    id = request.GET.get("id") or ""
    cols = request.GET.get("cols") or "2"
    try:
        cols = int(cols)
    except:
        cols = 2
    if cols <= 0:
        cols = 2
    if cols >= 6:
        cols = 6
    legend = request.GET.get("legend") or "off"
    cf = (request.GET.get("cf") or "AVERAGE").upper() # MAX, MIN, AVGRAGE, LAST
    sum = request.GET.get("sum") or "off"
    sumonly = request.GET.get("sumonly") or "off" #是否只显示求和
    graph_type = request.GET.get("graph_type") or GRAPH_TYPE_HOST
    nav_header = request.GET.get("nav_header") or "on"
    start = int(request.GET.get("start") or -3600)
    if start < 0:
        start = now + start
    end = int(request.GET.get("end") or 0)
    if end <= 0:
        end = now + end
    end = end - 60
    limit = int(request.GET.get("limit") or 0)
    page = int(request.GET.get("page") or 0)

    if not id:
        return HttpResponse("no graph id given")

    try:
        tmp_graph = TmpGraph.objects.get(id=id)
    except:
        tmp_graph = None
    if not tmp_graph:
        return HttpResponse("no graph which id is %s" % id)

    counters = tmp_graph.counters.split(COUNTER_DELIMITER)
    if not counters:
        return HttpResponse("no counters of %s" % id)
    counters = sorted(set(counters))

    endpoints = tmp_graph.endpoints.split(ENDPOINT_DELIMITER)
    if not endpoints:
        return HttpResponse("no endpoints of %s" % id)
    endpoints = sorted(set(endpoints))

    ret = {
        "units": "",
        "title": "",
        "series": []
    }
    ret['title'] = endpoints[0]
    e = endpoints[0]
    endpoint_counters = []
    for c in counters:
        endpoint_counters.append({
            "endpoint": e,
            "counter": c,
        })

    query_result = graph_query(endpoint_counters, cf, start, end)

    series = []
    for i in range(0, len(query_result)):
        x = query_result[i]
        try:
            xv = [(v["timestamp"]*1000, v["value"]) for v in x["Values"]]
            serie = {
                    "data": xv,
                    "name": query_result[i]["counter"],
                    "cf": cf,
                    "endpoint": query_result[i]["endpoint"],
                    "counter": query_result[i]["counter"],
            }
            series.append(serie)
        except:
            pass

    sum_serie = {
            "data": [],
            "name": "sum",
            "cf": cf,
            "endpoint": e,
            "counter": "sum",
    }
    if sum == "on" or sumonly == "on":
        sum = []
        tmp_ts = []
        max_size = 0
        for serie in series:
            serie_vs = [x[1] for x in serie["data"]]
            if len(serie_vs) > max_size:
                max_size = len(serie_vs)
                tmp_ts = [x[0] for x in serie["data"]]
            sum = merge_list(sum, serie_vs)
        sum_serie_data = []
        for i in range(0, max_size):
            sum_serie_data.append((tmp_ts[i], sum[i]))
        sum_serie['data'] = sum_serie_data

        series.append(sum_serie)

    if sumonly == "on":
        ret['series'] = [sum_serie, ]
    else:
        ret['series'] = series

    return JsonResponse(ret)


def multi_chart_data(request):
    now = int(time.time())
    id = request.GET.get("id") or ""
    cols = request.GET.get("cols") or "2"
    try:
        cols = int(cols)
    except:
        cols = 2
    if cols <= 0:
        cols = 2
    if cols >= 6:
        cols = 6
    legend = request.GET.get("legend") or "off"
    cf = (request.GET.get("cf") or "AVERAGE").upper() # MAX, MIN, AVGRAGE, LAST
    sum = request.GET.get("sum") or "off"
    sumonly = request.GET.get("sumonly") or "off" #是否只显示求和
    graph_type = request.GET.get("graph_type") or GRAPH_TYPE_HOST
    nav_header = request.GET.get("nav_header") or "on"
    start = int(request.GET.get("start") or -3600)
    if start < 0:
        start = now + start
    end = int(request.GET.get("end") or 0)
    if end <= 0:
        end = now + end
    end = end - 60
    limit = int(request.GET.get("limit") or 0)
    page = int(request.GET.get("page") or 0)

    if not id:
        return HttpResponse("no graph id given")

    tmp_graph = TmpGraph.objects.get(id=id)
    if not tmp_graph:
        return HttpResponse("no graph which id is %s" %id)

    counters = tmp_graph.counters.split(COUNTER_DELIMITER)
    if not counters:
        return HttpResponse("no counters of %s" %id)
    counters = sorted(set(counters))

    endpoints = tmp_graph.endpoints.split(ENDPOINT_DELIMITER)
    if not endpoints:
        return HttpResponse("no endpoints of %s, and tags:%s" %(id, tags))
    endpoints = sorted(set(endpoints))

    ret = {
        "units": "",
        "title": "",
        "series": []
    }

    endpoint_counters = []
    for e in endpoints:
        for c in counters:
            endpoint_counters.append({
                "endpoint": e,
                "counter": c,
            })
    query_result = graph_query(endpoint_counters, cf, start, end)

    series = []
    for i in range(0, len(query_result)):
        x = query_result[i]
        try:
            xv = [(v["timestamp"]*1000, v["value"]) for v in x["Values"]]
            serie = {
                    "data": xv,
                    "name": "%s %s" %(query_result[i]["endpoint"], query_result[i]["counter"]),
                    "cf": cf,
                    "endpoint": "",
                    "counter": "",
            }
            series.append(serie)
        except:
            pass

    sum_serie = {
            "data": [],
            "name": "sum",
            "cf": cf,
            "endpoint": "",
            "counter": "",
    }
    if sum == "on" or sumonly == "on":
        sum = []
        tmp_ts = []
        max_size = 0
        for serie in series:
            serie_vs = [x[1] for x in serie["data"]]
            if len(serie_vs) > max_size:
                max_size = len(serie_vs)
                tmp_ts = [x[0] for x in serie["data"]]
            sum = merge_list(sum, serie_vs)
        sum_serie_data = []
        for i in range(0, max_size):
            sum_serie_data.append((tmp_ts[i], sum[i]))
        sum_serie['data'] = sum_serie_data

        series.append(sum_serie)

    if sumonly == "on":
        ret['series'] = [sum_serie, ]
    else:
        ret['series'] = series

    return JsonResponse(ret)


@login_required(login_url='/login')
def charts(request):
    now = int(time.time())
    id = request.GET.get("id") or ""
    cols = request.GET.get("cols") or "2"
    try:
        cols = int(cols)
    except:
        cols = 2
    if cols <= 0:
        cols = 2
    if cols >= 6:
        cols = 6
    legend = request.GET.get("legend") or "off"
    cf = (request.GET.get("cf") or "AVERAGE").upper() # MAX, MIN, AVGRAGE, LAST
    sum = request.GET.get("sum") or "off"
    sumonly = request.GET.get("sumonly") or "off" #是否只显示求和
    graph_type = request.GET.get("graph_type") or GRAPH_TYPE_HOST
    nav_header = request.GET.get("nav_header") or "on"
    start = int(request.GET.get("start") or -3600)
    if start < 0:
        start = now + start
    end = int(request.GET.get("end") or 0)
    if end <= 0:
        end = now + end
    end = end - 60
    limit = int(request.GET.get("limit") or 0)
    page = int(request.GET.get("page") or 0)

    if not id:
        return HttpResponse("no graph id given")

    tmp_graph = TmpGraph.objects.get(id=id)
    if not tmp_graph:
        return HttpResponse("no graph which id is %s" % id)

    counters = tmp_graph.counters.split(COUNTER_DELIMITER) or []
    if not counters:
        return HttpResponse("no counters of %s" % id)
    counters = sorted(set(counters))

    endpoints = tmp_graph.endpoints.split(ENDPOINT_DELIMITER) or []
    if not endpoints:
        return HttpResponse("no endpoints of %s" % id)
    endpoints = sorted(set(endpoints))

    chart_urls = []
    chart_ids = []
    p = {
        "id": "",
        "legend": legend,
        "cf": cf,
        "sum": sum,
        "graph_type": graph_type,
        "nav_header": nav_header,
        "start": start,
        "end": end,
    }

    if graph_type == GRAPH_TYPE_KEY:

        for x in endpoints:
            es = x and ENDPOINT_DELIMITER.join(sorted(x)) or ""
            cs = counters and COUNTER_DELIMITER.join(sorted(counters)) or ""
            id_ = TmpGraph.objects.create(endpoints=x, counters=COUNTER_DELIMITER.join(counters),
                                          ck=hashlib.md5("%s:%s" % (es.encode("utf8"), cs.encode("utf8"))).hexdigest(),
                                          time=datetime.datetime.now()).id
            if not id_:
                continue

            p["id"] = id_
            chart_ids.append(int(id_))
            src = "/chart/h?" + urllib.urlencode(p)
            chart_urls.append(src)
    elif graph_type == GRAPH_TYPE_HOST:
        for x in counters:
            es = endpoints and ENDPOINT_DELIMITER.join(sorted(endpoints)) or ""
            cs = x and COUNTER_DELIMITER.join(sorted(x)) or ""
            id_ = TmpGraph.objects.create(endpoints=ENDPOINT_DELIMITER.join(endpoints), counters=x,
                                          ck=hashlib.md5("%s:%s" % (es.encode("utf8"), cs.encode("utf8"))).hexdigest(),
                                          time=datetime.datetime.now()).id
            if not id_:
                continue
            p["id"] = id_
            chart_ids.append(int(id_))
            src = "/chart/h?" + urllib.urlencode(p)
            chart_urls.append(src)
    else:
        es = endpoints and ENDPOINT_DELIMITER.join(sorted(endpoints)) or ""
        cs = counters and COUNTER_DELIMITER.join(sorted(counters)) or ""
        id_ = TmpGraph.objects.create(endpoints=ENDPOINT_DELIMITER.join(endpoints),
                                      counters=COUNTER_DELIMITER.join(counters),
                                      ck=hashlib.md5("%s:%s" % (es.encode("utf8"), cs.encode("utf8"))).hexdigest(),
                                      time=datetime.datetime.now()).id
        if id_:
            p["id"] = id_
            chart_ids.append(int(id_))
            src = "/chart/a?" + urllib.urlencode(p)
            chart_urls.append(src)
    return render_to_response("monitor/chart/multi_ng.html", locals(), RequestContext(request))


@login_required(login_url='/login')
def dash_screens(request):
    try:
        top_screens = DashboardScreen.objects.filter(pid='0')
        top_screens = sorted(top_screens, key=lambda x: x.name)
    except:
        top_screens = None

    current_top_screen = None

    dashheart_screens = DashboardScreenHeart.objects.filter(userid=request.user.id)
    heart_screens = []
    for heart in dashheart_screens:
        screen = DashboardScreen.objects.get(id=int(heart.screenid))
        heart_screens.append(screen)
    return render_to_response("monitor/screen/index.html", locals(), RequestContext(request))


@login_required(login_url='/login')
def dash_screen(request, sid):
    cols = request.GET.get("cols") or 2
    start = request.GET.get("start")
    end = request.GET.get("end")
    legend = request.GET.get("legend") or "off"
    heart = request.GET.get("heart") or None
    flash = request.GET.get("flash")or 0

    top_screens = DashboardScreen.objects.filter(pid='0')
    top_screens = sorted(top_screens, key=lambda x: x.name)

    screen = DashboardScreen.objects.get(id=sid)
    if not screen:
        return HttpResponse("no screen")
    if str(screen.pid) == '0':
        sub_screens = DashboardScreen.objects.filter(pid=str(sid))
        sub_screens = sorted(sub_screens, key=lambda x: x.name)
        current_top_screen = screen
        current_sub_screen = None
        return render_to_response("monitor/screen/top_screen.html", locals(), RequestContext(request))

    if not heart:
        try:
            DashboardScreenHeart.objects.get(userid=request.user.id, screenid=sid)
            heart = 'on'
        except:
            heart = 'off'
    else:
        if heart == 'on':
            DashboardScreenHeart.objects.get_or_create(userid=request.user.id, screenid=sid)
        elif heart == 'off':
            try:
                dash_heart = DashboardScreenHeart.objects.get(userid=request.user.id, screenid=sid)
                dash_heart.delete()
            except:
                pass
        else:
            pass
    pscreen = DashboardScreen.objects.get(id=screen.pid)
    sub_screens = DashboardScreen.objects.filter(pid=screen.pid)
    sub_screens = sorted(sub_screens, key=lambda x: x.name)
    graphs = DashboardGraph.objects.filter(screen_id=screen.id)

    all_graphs = []

    for graph in graphs:
        all_graphs.extend(generate_graph_urls(graph, start, end) or [])

    all_graphs = sorted(all_graphs, key=lambda x: x.position)
    current_top_screen = pscreen
    current_sub_screen = screen
    return render_to_response("monitor/screen/screen.html", locals(), RequestContext(request))


@login_required(login_url='/login')
def dash_screen_add(request):
    if request.method == "POST":
        name = request.POST.get("screen_name")
        pid = request.POST.get("pid", '0')
        screen, _ = DashboardScreen.objects.get_or_create(pid=pid, name=name,
                                                          defaults={
                                                              'time': datetime.datetime.now()
                                                          })
        return HttpResponseRedirect("/monitor/screen/%s/" % screen.id)
    else:
        pid = request.GET.get("pid", '0')
        screen = DashboardScreen.objects.filter(pid=pid)
        return render_to_response("monitor/screen/add.html", locals(), RequestContext(request))


@login_required(login_url='/login')
def dash_graph_add(request, sid):
    all_screens = DashboardScreen.objects.all()
    top_screens = [x for x in all_screens if x.pid == '0']
    children = []
    for t in top_screens:
        children.append([x for x in all_screens if x.pid == str(t.id)])

    screen = DashboardScreen.objects.get(id=sid)
    if not screen:
        return HttpResponse("no screen")
    pscreen = DashboardScreen.objects.get(id=screen.pid)

    if request.method == "POST":
        title = request.POST.get("title")

        hosts = request.POST.get("hosts", "").strip()
        hosts = hosts and hosts.split("\n") or []
        hosts = [x.strip() for x in hosts]

        counters = request.POST.get("counters", "").strip()
        counters = counters and counters.split("\n") or []
        counters = [x.strip() for x in counters]

        timespan = request.POST.get("timespan", 3600)
        graph_type = request.POST.get("graph_type", 'h')
        method = request.POST.get("method", '').upper()
        position = request.POST.get("position", 0)

        graph, _ = DashboardGraph.objects.get_or_create(title=title, hosts=ENDPOINT_DELIMITER.join(hosts),
                                                        counters=COUNTER_DELIMITER.join(counters), screen_id=sid,
                                                        timespan=timespan, graph_type=graph_type,
                                                        method=method, position=position)
        return HttpResponseRedirect("/monitor/screen/%s/" % sid)

    else:
        gid = request.GET.get("gid")
        graph = gid and DashboardGraph.objects.get(id=gid)
        return render_to_response("monitor/screen/graph_add.html", locals(), RequestContext(request))


@login_required(login_url='/login')
def dash_screen_edit(request, sid):
    try:
        screen = DashboardScreen.objects.get(id=sid)
    except:
        screen =None
    if not screen:
        return HttpResponse("no such screen")

    if request.method == "POST":
        screen_name = request.POST.get("screen_name")
        screen.name = screen_name
        screen.save()
        return HttpResponseRedirect("/monitor/screen/%s" % screen.id)
    else:
        return render_to_response("monitor/screen/edit.html", locals(), RequestContext(request))


@login_required(login_url='/login')
def dash_screen_delete(request, sid):
    try:
        screen = DashboardScreen.objects.get(id=sid)
    except:
        screen = None
    if not screen:
        return HttpResponse("no such screen")
    screen.delete()
    try:
        DashboardScreenHeart.objects.filter(screenid=sid).delete()
    except:
        pass

    return HttpResponseRedirect("/monitor/screen/")


@login_required(login_url='/login')
def dash_screen_clone(request, sid):
    try:
        screen = DashboardScreen.objects.get(id=sid)
    except:
        screen = None
    if not screen:
        return HttpResponse("no such screen")

    if request.method == "POST":
        screen_name = request.POST.get("screen_name")
        with_graph = request.POST.get("with_graph")

        new_s = DashboardScreen.objects.create(pid=screen.pid, name=screen_name, time=datetime.datetime.now())
        if not new_s:
            return HttpResponse("创建screen失败了")

        if with_graph:
            old_graphs = DashboardGraph.objects.filter(screen_id=sid)
            for o in old_graphs:
                DashboardGraph.objects.create(title=o.title, hosts=o.hosts, counters=o.counters,
                                              screen_id=new_s.id, timespan=o.timespan, graph_type=o.graph_type,
                                              method=o.method, position=o.position)

        return HttpResponseRedirect("/monitor/screen/%s/" % new_s.id)
    else:
        return render_to_response("monitor/screen/clone.html", locals(), RequestContext(request))


@login_required(login_url='/login')
def dash_graph_edit(request, gid):
    error = ""
    try:
        graph = DashboardGraph.objects.get(id=gid)
    except:
        graph = None
    if not graph:
        return HttpResponse("no graph")

    all_screens = DashboardScreen.objects.all()

    top_screens = [x for x in all_screens if x.pid == '0']
    children = []
    for t in top_screens:
        children.append([x for x in all_screens if x.pid == str(t.id)])
    children = [x for x in all_screens if x.pid != '0']
    try:
        screen = DashboardScreen.objects.get(id=graph.screen_id)
    except:
        screen = None
    if not screen:
        return HttpResponse("no screen")
    pscreen = DashboardScreen.objects.get(id=screen.pid)
    if request.method == "POST":
        ajax = request.POST.get("ajax", "")
        screen_id = request.POST.get("screen_id")
        title = request.POST.get("title", "").strip()

        hosts = request.POST.get("hosts", "").strip()
        hosts = hosts and hosts.split("\n") or []
        hosts = [x.strip() for x in hosts]

        counters = request.POST.get("counters", "").strip()
        counters = counters and counters.split("\n") or []
        counters = [x.strip() for x in counters]

        timespan = request.POST.get("timespan", 3600)
        graph_type = request.POST.get("graph_type", 'h')
        method = request.POST.get("method", '').upper()
        position = request.POST.get("position", 0)

        graph.title = title
        graph.hosts = ENDPOINT_DELIMITER.join(hosts)
        graph.counters = COUNTER_DELIMITER.join(counters)
        graph.screen_id = screen_id
        graph.timespan = timespan
        graph.graph_type = graph_type
        graph.position = position
        graph.save()

        error = u"修改成功了"
        return HttpResponseRedirect("/monitor/screen/%s/" % screen_id)

    else:
        ajax = request.GET.get("ajax", "")
        return render_to_response("monitor/screen/graph_edit.html", locals(), RequestContext(request))


@login_required(login_url='/login')
def dash_graph_delete(request, gid):
    try:
        graph = DashboardGraph.objects.get(id=gid)
    except:
        graph = None
    if not graph:
        return HttpResponse("no such graph")
    graph.delete()
    return HttpResponseRedirect("/monitor/screen/%s/" % graph.screen_id)
