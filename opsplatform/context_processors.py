from account.models import User
from asset.models import Asset
from opsplatform.api import *
import settings
from MySQLdb import ProgrammingError


def name_proc(request):
    dashboard_url = settings.DASHBOARD_URL
    portal_url = settings.PORTAL_URL
    alarm_url = settings.ALARM_URL
    grafana_url = settings.GRAFANA_URL

    user_total_num = User.objects.all().count()
    user_active_num = User.objects.filter(is_active=True).count()
    host_total_num = Asset.objects.all().count()
    host_active_num = Asset.objects.filter(is_active=True).count()
    request.session.set_expiry(3600)

    info_dic = {
                'dashboard_url': dashboard_url,
                'portal_url': portal_url,
                'alarm_url': alarm_url,
                'grafana_url': grafana_url,
                'user_total_num': user_total_num,
                'user_active_num': user_active_num,
                'host_total_num': host_total_num,
                'host_active_num': host_active_num,
                }

    return info_dic
