# encoding: utf-8

"""
@version:
@author: liriqiang
@file: urls.py
@time: 16-7-25 上午11:36
"""

from express.models import PublishTask
from django.views.decorators.csrf import csrf_exempt
import json
from opsplatform.api import JsonResponse


@csrf_exempt
def publish_task_create(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            data = data.get('data')
            print data
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

