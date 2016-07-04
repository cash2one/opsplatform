from django.db import models
from opsplatform.until import UnixTimestampField


class TmpGraph(models.Model):
    endpoints = models.CharField('Endpoint', max_length=10240, default='')
    counters = models.CharField('Counters', max_length=10240, default='')
    ck = models.CharField('ck', max_length=32, default='')
    time = UnixTimestampField(db_column='time_', auto_created=True)

    def __unicode__(self):
        return "<TmpGraph id=%s, endpoints=%s, counters=%s>" % (self.id, self.endpoints, self.counters)


class DashboardScreen(models.Model):
    pid = models.CharField('PID', max_length=100)
    name = models.CharField(max_length=100)
    time = UnixTimestampField(auto_created=True)

    def __unicode__(self):
        return "<DashboardScreen id=%s, name=%s, pid=%s>" % (self.id, self.name, self.pid)


class DashboardGraph(models.Model):
    title = models.CharField('title', max_length=100)
    hosts = models.CharField('hosts', max_length=100)
    counters = models.CharField('counters', max_length=100)
    screen_id = models.CharField('screen_id', max_length=100)
    timespan = models.IntegerField('timespan', default=3600)
    graph_type = models.CharField('graph_type', max_length=10, default='h')
    method = models.CharField('method', max_length=100)
    position = models.IntegerField('position', default=0)

    def __unicode__(self):
        return "<DashboardGraph id=%s, title=%s, screen_id=%s>" % (self.id, self.title, self.screen_id)


class DashboardScreenHeart(models.Model):
    userid = models.CharField(max_length=100)
    screenid = models.CharField(max_length=100)
