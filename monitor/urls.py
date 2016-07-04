"""opsplatform URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.9/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url
from monitor.views import *


urlpatterns = [
    url(r'^index/$', index, name='monitor_index'),
    url(r'^chart/$', chart, name='chart'),
    url(r'^chart/h$', multi_endpoints_chart_data, name='multi_endpoints_chart_data'),
    url(r'^chart/k$', multi_counters_chart_data, name='multi_counters_chart_data'),
    url(r'^chart/a$', multi_chart_data, name='multi_chart_data'),
    url(r'^chart/big$', chart_big, name='chart_big'),
    url(r'^charts/$', charts, name='charts'),

    url(r'^screen/$', dash_screens, name='dash_screens'),
    url(r'^screen/(?P<sid>[0-9]*)/$', dash_screen, name='dash_screen'),
    url(r'^screen/add/$', dash_screen_add, name='dash_screen_add'),
    url(r'^screen/(?P<sid>[0-9]*)/graph/$', dash_graph_add, name='dash_graph_add'),
    url(r'^screen/(?P<sid>[0-9]*)/edit/$', dash_screen_edit, name='dash_screen_edit'),
    url(r'^screen/(?P<sid>[0-9]*)/delete/$', dash_screen_delete, name='dash_screen_delete'),
    url(r'^screen/(?P<sid>[0-9]*)/clone/$', dash_screen_clone, name='dash_screen_clone'),

    url(r'^graph/(?P<gid>[0-9]*)/edit/$', dash_graph_edit, name='dash_graph_edit'),
    url(r'^graph/(?P<gid>[0-9]*)/delete/$', dash_graph_delete, name='dash_graph_delete'),

    url(r'^api/endpoints/$', api_endpoints, name='api_endpoints'),
    url(r'^api/counters/$', api_counters, name='api_counters'),
]
