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
    (4, '商家系统'),
    (5, '开放接口'),
    (6, '活动系统'),
    (7, '人人快递优惠券服务'),
    (8, '微信端'),
    (9, '裹裹对接系统'),
    (10, '客服系统'),
    (11, '推送系统'),
    (12, '财务系统(Java)'),
    (13, '财务系统(PHP)'),
    (14, '帮买（精品购）java接口'),
    (15, '商家管理店铺商品-java'),
    (-1, '综合发布')
)

ENV = (
    (1, '线上环境'),
    (2, '模拟环境'),
    (3, '第三方对接环境'),
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
    qa_note = models.TextField(u'测试评估建议', null=True)
    owner = models.CharField(u'项目负责人', max_length=100)
    submit_time = models.DateTimeField(u'提交时间', null=True)
    submit_by = models.CharField(u'提交人', max_length=100, null=True)
    approval_time = models.DateTimeField(u'审核时间', null=True)
    approval_by = models.CharField(u'审核人', max_length=100, null=True)
    publish_time = models.CharField(u'计划发版时间', max_length=50, null=True)
    is_auto_deploy = models.CharField(u'是否自动发布', max_length=100, null=True)
    idc = models.CharField(u'发布类型', max_length=1000, null=True)
    deploy_time = models.DateTimeField(u'发布时间', null=True)
    deploy_by = models.CharField(u'发布人', max_length=100, null=True)
    status = models.CharField(u'状态', max_length=100)
    create_time = models.DateTimeField(u'创建时间', auto_now_add=True)
    create_by = models.CharField(u'创建人', max_length=100)

    def __unicode__(self):
        return self.seq_no


class PublishTaskDeploy(models.Model):
    publish_task = models.ForeignKey(PublishTask)
    deploy_progress = models.CharField(u'发布进度', max_length=100, null=True)
    deploy_total = models.CharField(u'发布所需步骤', max_length=100, null=True)
    deploy_info = models.TextField(u'发布过程输出', null=True)


STYLE = (
    (1, '人人快递'),
    (2, '自由快递人'),
)


PLATFORM = (
    (1, 'Android'),
    (2, 'IOS'),
)


class AppPublishTask(models.Model):
    seq_no = models.CharField(u'发布序列号', max_length=50, unique=True)
    env = models.CharField(u'环境类型', max_length=50)
    style = models.CharField(u'类型', max_length=100)
    platform = models.CharField(u'平台', max_length=100)
    version = models.CharField(u'版本号', max_length=100)
    owner = models.CharField(u'项目负责人', max_length=100)
    update_remark = models.TextField(u'更新理由')

    client_apk_path = models.CharField(u'APK', max_length=1000, null=True)
    client_sys_AndroidPublishVersion = models.CharField(max_length=100, null=True)
    client_sys_IOSPublishVersion = models.CharField(max_length=100, null=True)
    client_sys_Androidisforcedupdate = models.CharField(max_length=100, null=True)
    client_sys_IOSisforcedupdate = models.CharField(max_length=100, null=True)
    client_config_iossjversion = models.CharField(max_length=100, null=True)
    client_config_iosUpdateRemark = models.TextField(null=True)
    client_config_iosverremark = models.TextField(null=True)
    client_config_androidversion = models.CharField(max_length=100, null=True)
    client_config_androidsjversion = models.CharField(max_length=100, null=True)
    client_config_downloadandroidpath = models.CharField(max_length=1000, null=True)
    client_config_androidverremark = models.TextField(null=True)
    client_config_androidsUpdateRemark = models.TextField(null=True)

    courier_apk_path = models.CharField(max_length=1000, null=True)
    courier_sys_AndroidPublishVersion = models.CharField(max_length=100, null=True)
    courier_sys_IOSPublishVersion = models.CharField(max_length=100, null=True)
    courier_sys_Androidisforcedupdate = models.CharField(max_length=100, null=True)
    courier_sys_IOSisforcedupdate = models.CharField(max_length=100, null=True)
    courier_config_iossjversion = models.CharField(max_length=100, null=True)
    courier_config_iosUpdateRemark = models.TextField(null=True)
    courier_config_iosverremark = models.TextField(null=True)
    courier_config_androidversion = models.CharField(max_length=100, null=True)
    courier_config_androidsjversion = models.CharField(max_length=100, null=True)
    courier_config_downloadandroidpath = models.CharField(max_length=1000, null=True)
    courier_config_androidverremark = models.TextField(null=True)
    courier_config_androidsUpdateRemark = models.TextField(null=True)

    approval_time = models.DateTimeField(u'审核时间', null=True)
    approval_by = models.CharField(u'审核人', max_length=100, null=True)
    publish_time = models.CharField(u'计划发版时间', max_length=50, null=True)
    submit_time = models.DateTimeField(u'提交时间', null=True)
    submit_by = models.CharField(u'提交人', max_length=100, null=True)
    deploy_time = models.DateTimeField(u'发布时间', null=True)
    deploy_by = models.CharField(u'发布人', max_length=100, null=True)
    status = models.CharField(u'状态', max_length=100)
    create_time = models.DateTimeField(u'创建时间', auto_now_add=True)
    create_by = models.CharField(u'创建人', max_length=100)

    def __unicode__(self):
        return self.seq_no


YES_NO = (
    ('yes', u'是'),
    ('no', u'否'),
)


MVN_ENV = (
    ('1', 'pro'),
    ('2', 'sim'),
    ('3', 'code')
)


LANGUAGE_TYPE = (
    ('Java', 'Java'),
    ('PHP', 'PHP'),
    ('GO', 'GO'),
    (u'前端', u'前端'),
)


class Project(models.Model):
    name = models.CharField(u'项目名称', max_length=100)
    code = models.CharField(u'项目编号', max_length=100)
    language_type = models.CharField(u'开发语言', max_length=100)
    git_url = models.CharField(u'Git地址', max_length=200)
    git_branch = models.CharField(u'Git Branch', max_length=100)
    env = models.CharField(u'发布环境', max_length=100)
    is_full = models.CharField(u'是否全量更新', max_length=100)
    idc = models.CharField(u'机房', max_length=100)
    host = models.CharField(u'服务器IP', max_length=100)
    src = models.CharField(u'源地址', max_length=200)
    dest = models.CharField(u'部署路径', max_length=200)
    tomcat_num = models.CharField(u'Tomcat编号', max_length=10)
    backup_dir = models.CharField(u'备份路径', max_length=200)
    ignore_setup = models.TextField(u'忽略上传文件')

    def __unicode__(self):
        return self.name
