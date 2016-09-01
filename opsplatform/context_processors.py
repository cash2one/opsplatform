from account.models import User
from asset.models import Asset
from opsplatform.api import *
import settings
from MySQLdb import ProgrammingError


def name_proc(request):
    portal_url = settings.PORTAL_URL
    alarm_url = settings.ALARM_URL
    deploy_url = settings.DEPLOY_URL
    config_url = settings.CONFIG_URL
    virtmgr_url = settings.VIRTMGR_URL
    logserver_url = settings.LOGSERVER_URL
    logalarm_url = settings.LOGALARM_URL
    user_total_num = User.objects.all().count()
    user_active_num = User.objects.filter(is_active=True).count()
    host_total_num = Asset.objects.all().count()
    host_active_num = Asset.objects.filter(is_active=True).count()
    request.session.set_expiry(36000)

    info_dic = {
                'deploy_url': deploy_url,
                'config_url': config_url,
                'virtmgr_url': virtmgr_url,
                'portal_url': portal_url,
                'alarm_url': alarm_url,
                'logserver_url': logserver_url,
                'logalarm_url': logalarm_url,
                'user_total_num': user_total_num,
                'user_active_num': user_active_num,
                'host_total_num': host_total_num,
                'host_active_num': host_active_num,
                }

    return info_dic
