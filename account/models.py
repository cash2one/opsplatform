# encoding: utf-8

"""
@version:
@author: liriqiang
@file: models.py
@time: 16-6-2 下午5:29
"""


from __future__ import unicode_literals

from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    name = models.CharField(max_length=80)
    uuid = models.CharField(max_length=100)
    ssh_key_pwd = models.CharField(max_length=200)
    phone = models.CharField(max_length=11, null=True, default='')
    qq = models.CharField(max_length=20, null=True, default='')

    def __unicode__(self):
        return self.username


class Role(models.Model):

    class Meta:
        permissions = (
            ("perm_can_view_account", u"用户权限管理"),

            ("perm_can_add_group", "新增用户组"),
            ("perm_can_change_group", "修改用户组"),
            ("perm_can_delete_group", "删除用户组"),
            ("perm_can_view_group", "查看用户组"),

            ("perm_can_add_user", "新增用户"),
            ("perm_can_change_user", "修改用户"),
            ("perm_can_delete_user", "删除用户"),
            ("perm_can_view_user", u"查看用户"),


            ("perm_can_view_assets", u"资产管理"),

            ("perm_can_add_assetgroup", "新增资产组"),
            ("perm_can_change_assetgroup", "修改资产组"),
            ("perm_can_delete_assetgroup", "删除资产组"),
            ("perm_can_view_assetgroup", "查看资产组"),

            ("perm_can_add_asset", "新增资产"),
            ("perm_can_change_asset", "修改资产"),
            ("perm_can_delete_asset", "删除资产"),
            ("perm_can_view_asset", "查看资产"),

            ("perm_can_add_idc", "新增机房"),
            ("perm_can_change_idc", "修改机房"),
            ("perm_can_delete_idc", "删除机房"),
            ("perm_can_view_idc", "查看机房"),


            ("perm_can_view_perm", "授权管理"),

            ("perm_can_add_permsudo", "新增Sudo"),
            ("perm_can_change_permsudo", "修改Sudo"),
            ("perm_can_delete_permsudo", "删除Sudo"),
            ("perm_can_view_permsudo", "查看Sudo"),

            ("perm_can_add_permrole", "新增系统用户"),
            ("perm_can_change_permrole", "修改系统用户"),
            ("perm_can_delete_permrole", "删除系统用户"),
            ("perm_can_view_permrole", "查看系统用户"),

            ("perm_can_add_permrule", "新增授权规则"),
            ("perm_can_change_permrule", "修改授权规则"),
            ("perm_can_delete_permrule", "删除授权规则"),
            ("perm_can_view_permrule", "查看授权规则"),

            ("perm_can_conn_asset", "SSH连接资产"),
            ("perm_can_exec_cmd", "执行批量命令"),
            ("perm_can_role_push", "推送系统用户"),

            ("perm_can_view_log", "查看日志信息"),
            ("perm_can_upload_download_file", "上传下载文件"),
            ("perm_can_view_dashboard", "查看统计日志"),

            ("perm_can_view_monitor", "监控服务"),
            ("perm_can_view_portal", "查看监控Portal"),
            ("perm_can_view_screen", "查看监控趋势图"),
            ("perm_can_view_alarm", "查看未恢复的报警"),

            ("perm_can_view_deploy", "查看代码发布"),
            ("perm_can_view_config", "产看配置中心"),
            ("perm_can_view_virtmgr", "查看虚拟化管理平台"),
        )

