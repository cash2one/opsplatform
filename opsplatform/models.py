# encoding: utf-8

"""
@version: 
@author: liriqiang
@file: models.py
@time: 16-6-2 下午5:28
"""

from django.db import models
from account.models import User
import time


class Note(models.Model):
    text = models.TextField()