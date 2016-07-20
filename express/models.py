# encoding: utf-8

"""
@version:
@author: liriqiang
@file: urls.py
@time: 16-7-19 上午10:00
"""

from django.db import models


class PublishTask(models.Model):
    seq_no = models.CharField(u'发布序列号', max_length=50)
    product = models.CharField(u'生产线', max_length=100)
    project = models.CharField(u'产品名称', max_length=100)
    type = models.CharField(u'环境类型', max_length=50)
    version = models.CharField(u'版本', max_length=50)
    update_remark = models.TextField(u'更新理由')
    code_dir = models.TextField(u'代码地址')
    settings = models.TextField(u'环境设置')
    update_note = models.TextField(u'更新说明')
    owner = models.CharField(u'项目负责人', max_length=100)
    submit_time = models.DateTimeField(u'提交时间')
    submit_by = models.CharField(u'提交人', max_length=100)
    approval_time = models.DateTimeField(u'审核时间', null=True)
    approval_by = models.CharField(u'审核人', max_length=100, null=True)
    deploy_time = models.DateTimeField(u'发布时间', null=True)
    deploy_by = models.CharField(u'发布人', max_length=100, null=True)
    status = models.CharField(u'状态', max_length=100)