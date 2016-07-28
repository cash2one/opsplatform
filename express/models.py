# encoding: utf-8

"""
@version:
@author: liriqiang
@file: urls.py
@time: 16-7-19 上午10:00
"""

from django.db import models


LINE = (
    (1, '人人快递'),
    (2, '自由快递人'),
    (3, '运营系统'),
    (1, '人人快递'),
    (2, '自由快递人'),
    (3, '运营系统'),
    (4, '商家系统'),
    (5, '开放接口'),
    (6, '活动系统'),
    (7, '人人快递优惠券服务'),
)

ENV = (
    (1, '线上环境'),
    (2, '模拟环境'),
)

STATUS = (
    (1, '未提交'),
    (2, '已提交'),
    (3, '已审核'),
    (4, '已发布'),
    (5, '已回滚'),
    (6, '已驳回'),
)


class PublishTask(models.Model):
    seq_no = models.CharField(u'发布序列号', max_length=50, unique=True)
    product = models.CharField(u'产品线', max_length=100, null=True)
    project = models.CharField(u'产品名称', max_length=100)
    env = models.CharField(u'环境类型', max_length=50)
    version = models.CharField(u'版本', max_length=50)
    update_remark = models.TextField(u'更新理由')
    code_dir = models.TextField(u'代码地址', null=True)
    code_tag = models.CharField(u'Tag', max_length=100, null=True)
    database_update = models.TextField(u'数据库更新说明', null=True)
    upload_sql = models.CharField(u'更新SQL文件', max_length=1000, null=True)
    settings = models.TextField(u'环境设置', null=True)
    update_note = models.TextField(u'更新说明', null=True)
    owner = models.CharField(u'项目负责人', max_length=100)
    submit_time = models.DateTimeField(u'提交时间', null=True)
    submit_by = models.CharField(u'提交人', max_length=100, null=True)
    approval_time = models.DateTimeField(u'审核时间', null=True)
    approval_by = models.CharField(u'审核人', max_length=100, null=True)
    publish_time = models.CharField(u'计划发版时间', max_length=50, null=True)
    deploy_time = models.DateTimeField(u'发布时间', null=True)
    deploy_by = models.CharField(u'发布人', max_length=100, null=True)
    status = models.CharField(u'状态', max_length=100)
    create_time = models.DateTimeField(u'创建时间', auto_now_add=True)
    create_by = models.CharField(u'创建人', max_length=100)

    def __unicode__(self):
        return self.seq_no

