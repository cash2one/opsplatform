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
from asset.views import *


urlpatterns = [
    url(r'^asset/add/$', asset_add, name='asset_add'),
    url(r"^asset/add_batch/$", asset_add_batch, name='asset_add_batch'),
    url(r'^asset/list/$', asset_list, name='asset_list'),
    url(r'^asset/del/$', asset_del, name='asset_del'),
    url(r"^asset/detail/$", asset_detail, name='asset_detail'),
    url(r'^asset/edit/$', asset_edit, name='asset_edit'),
    url(r'^asset/edit_batch/$', asset_edit_batch, name='asset_edit_batch'),
    url(r'^asset/update/$', asset_update, name='asset_update'),
    url(r'^asset/update_batch/$', asset_update_batch, name='asset_update_batch'),
    url(r'^asset/upload/$', asset_upload, name='asset_upload'),

    url(r'^group/del/$', group_del, name='asset_group_del'),
    url(r'^group/add/$', group_add, name='asset_group_add'),
    url(r'^group/list/$', group_list, name='asset_group_list'),
    url(r'^group/edit/$', group_edit, name='asset_group_edit'),

    url(r'^idc/add/$', idc_add, name='idc_add'),
    url(r'^idc/list/$', idc_list, name='idc_list'),
    url(r'^idc/edit/$', idc_edit, name='idc_edit'),
    url(r'^idc/del/$', idc_del, name='idc_del'),
]
