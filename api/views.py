# encoding: utf-8

"""
@version:
@author: liriqiang
@file: urls.py
@time: 16-7-25 上午11:36
"""

from express.models import *
from django.views.decorators.csrf import csrf_exempt
import json
from opsplatform.api import *


@csrf_exempt
def publish_task_create(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            data = data.get('data')
            obj, created = PublishTask.objects.get_or_create(seq_no=data.get('seq_no'),
                                                             defaults={
                                                                 'product': data.get('product'),
                                                                 'project': data.get('project'),
                                                                 'env': data.get('env'),
                                                                 'version': data.get('version'),
                                                                 'update_remark': data.get('update_remark'),
                                                                 'code_dir': data.get('code_dir'),
                                                                 'code_tag': data.get('code_tag'),
                                                                 'database_update': data.get('database_update'),
                                                                 'upload_sql': data.get('upload_sql'),
                                                                 'settings': data.get('settings'),
                                                                 'update_note': data.get('update_note'),
                                                                 'owner': data.get('owner'),
                                                                 'submit_time': data.get('submit_time'),
                                                                 'submit_by': data.get('submit_by'),
                                                                 'approval_time': data.get('approval_time'),
                                                                 'approval_by': data.get('approval_by'),
                                                                 'publish_time': data.get('publish_time'),
                                                                 'status': data.get('status'),
                                                                 'create_time': data.get('create_time'),
                                                                 'create_by': data.get('create_by'),
                                                             })
        except Exception, e:
            print e
            return JsonResponse({'msg': "parameter format invalid.", 'code': 0})
    else:
        return JsonResponse({'msg': "not POST method.", 'code': 0})
    return JsonResponse({'msg': 'success', 'code': 1})


@csrf_exempt
def app_publish_task_create(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            data = data.get('data')
            obj, created = AppPublishTask.objects.get_or_create(seq_no=data.get('seq_no'),
                                                                defaults={
                                                                    'env': data.get('env'),
                                                                    'style': data.get('style'),
                                                                    'platform': data.get('platform'),
                                                                    'version': data.get('version'),
                                                                    'owner': data.get('owner'),
                                                                    'update_remark': data.get('update_remark'),
                                                                    'client_apk_path': data.get('client_apk_path'),
                                                                    'client_sys_AndroidPublishVersion': data.get('client_sys_AndroidPublishVersion'),
                                                                    'client_sys_IOSPublishVersion': data.get('client_sys_IOSPublishVersion'),
                                                                    'client_sys_Androidisforcedupdate': data.get('client_sys_Androidisforcedupdate'),
                                                                    'client_sys_IOSisforcedupdate': data.get('client_sys_IOSisforcedupdate'),
                                                                    'client_config_iossjversion': data.get('client_config_iossjversion'),
                                                                    'client_config_iosUpdateRemark': data.get('client_config_iosUpdateRemark'),
                                                                    'client_config_iosverremark': data.get('client_config_iosverremark'),
                                                                    'client_config_androidversion': data.get('client_config_androidversion'),
                                                                    'client_config_androidsjversion': data.get('client_config_androidsjversion'),
                                                                    'client_config_downloadandroidpath': data.get('client_config_downloadandroidpath'),
                                                                    'client_config_androidverremark': data.get('client_config_androidverremark'),
                                                                    'client_config_androidsUpdateRemark': data.get('client_config_androidsUpdateRemark'),
                                                                    'courier_apk_path': data.get('courier_apk_path'),
                                                                    'courier_sys_AndroidPublishVersion': data.get('courier_sys_AndroidPublishVersion'),
                                                                    'courier_sys_IOSPublishVersion': data.get('courier_sys_IOSPublishVersion'),
                                                                    'courier_sys_Androidisforcedupdate': data.get('courier_sys_Androidisforcedupdate'),
                                                                    'courier_sys_IOSisforcedupdate': data.get('courier_sys_IOSisforcedupdate'),
                                                                    'courier_config_iossjversion': data.get('courier_config_iossjversion'),
                                                                    'courier_config_iosUpdateRemark': data.get('courier_config_iosUpdateRemark'),
                                                                    'courier_config_iosverremark': data.get('courier_config_iosverremark'),
                                                                    'courier_config_androidversion': data.get('courier_config_androidversion'),
                                                                    'courier_config_androidsjversion': data.get('courier_config_androidsjversion'),
                                                                    'courier_config_downloadandroidpath': data.get('courier_config_downloadandroidpath'),
                                                                    'courier_config_androidverremark': data.get('courier_config_androidverremark'),
                                                                    'courier_config_androidsUpdateRemark': data.get('courier_config_androidsUpdateRemark'),
                                                                    'approval_time': data.get('approval_time'),
                                                                    'approval_by': data.get('approval_by'),
                                                                    'publish_time': data.get('publish_time'),
                                                                    'submit_time': data.get('submit_time'),
                                                                    'submit_by': data.get('submit_by'),
                                                                    'status': data.get('status'),
                                                                    'create_time': data.get('create_time'),
                                                                    'create_by': data.get('create_by'),
                                                             })
        except Exception, e:
            print e
            return JsonResponse({'msg': "parameter format invalid.", 'code': 0})
    else:
        return JsonResponse({'msg': "not POST method.", 'code': 0})
    return JsonResponse({'msg': 'success', 'code': 1})


@csrf_exempt
def get_projects(request):
    env = request.GET.get('env', '')
    projects = []
    if not env:
        for i in Project.objects.all():
            projects.append(i.name)
    else:
        for i in Project.objects.filter(env=env):
            projects.append(i.name)

    return JsonResponse({"msg": "", "projects": projects})
