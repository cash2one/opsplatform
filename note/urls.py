# encoding: utf-8

"""
@version: 
@author: liriqiang
@file: urls.py
@time: 16-7-11 下午5:51
"""

from django.conf.urls import patterns, include, url
from note.views import *

urlpatterns = [
    url(r'^list/$', note_list, name='note_list'),
    url(r'^add/$', note_add, name='note_add'),
    url(r'^del/$', note_del, name='note_del'),
]