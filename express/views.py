# encoding: utf-8

"""
@version:
@author: liriqiang
@file: urls.py
@time: 16-7-19 上午10:00
"""

from opsplatform.api import *
from models import *
from django.utils import timezone
from opsplatform import settings


@require_permission('account.perm_can_view_publish_task')
def publish_task_list(request):
    """
    list publish task
    发布任务列表
    """
    header_title, path1, path2 = '查看发布任务', '发布任务管理', '查看发布任务'
    keyword = request.GET.get('search', '')
    publish_task_list = PublishTask.objects.all().order_by('-seq_no')
    task_id = request.GET.get('id', '')
    status_all = list(STATUS)
    env_all = list(ENV)
    env_value = request.GET.get('env', '')
    status_value = request.GET.get('status', '3')

    if env_value:
        publish_task_list = publish_task_list.filter(env=env_value)
    if status_value:
        publish_task_list = publish_task_list.filter(status=status_value)
    if keyword:
        publish_task_list = publish_task_list.filter(name__icontains=keyword)

    publish_task_list, p, publish_tasks, page_range, current_page, show_first, show_end = pages(publish_task_list, request)
    return render_to_response('express/publish_task_list.html', locals(), RequestContext(request))


@require_permission('account.perm_can_view_publish_task')
def publish_task_detail(request):
    header_title, path1, path2 = '发布任务详情', '查看发布任务', '发布任务详情'
    task_id = request.GET.get('id', '')
    if not task_id:
        return HttpResponseRedirect(reverse('publish_task_list'))
    publish_task = get_object(PublishTask, id=task_id)
    if not publish_task:
        return HttpResponseRedirect(reverse('publish_task_list'))
    return render_to_response('express/publish_task_detail.html', locals(), RequestContext(request))


@require_permission('account.perm_can_trash_publish_task')
def publish_task_trash(request):
    task_id = request.GET.get('id', '')
    if not task_id:
        return HttpResponseRedirect(reverse('publish_task_list'))
    publish_task = get_object(PublishTask, id=task_id)
    if not publish_task:
        return HttpResponseRedirect(reverse('publish_task_list'))
    publish_task.status = 6
    publish_task.save()
    # 调用接口
    data = api_call('%s%s' % (settings.PUBLISH_CENTER_URL, settings.PUBLISH_TASK_STATUS_UPDATE),
                    json.dumps({"seq_no": publish_task.seq_no, "status": publish_task.status,
                                "deploy_time": publish_task.deploy_time.strftime("%Y-%m-%d %H:%M:%S") if publish_task.deploy_time else '',
                                "deploy_by": publish_task.deploy_by}), 'POST',
                    {'Content-Type': 'application/json'})
    if data and data.get('code') == -1:
        error = data.get('msg')
        return HttpResponse(error)
    if not data:
        error = u'无法打开目标网址,请联系系统开发人员!'
        return HttpResponse(error)
    return HttpResponseRedirect(reverse('publish_task_list'))


@require_permission('account.perm_can_deploy_publish_task')
def publish_task_deploy(request):
    task_id = request.GET.get('id', '')
    if not task_id:
        return HttpResponseRedirect(reverse('publish_task_list'))
    publish_task = get_object(PublishTask, id=task_id)
    if not publish_task:
        return HttpResponseRedirect(reverse('publish_task_list'))
    publish_task.status = 4
    publish_task.deploy_time = datetime.datetime.now()
    publish_task.deploy_by = request.user.username
    publish_task.save()
    # 调用接口
    data = api_call('%s%s' % (settings.PUBLISH_CENTER_URL, settings.PUBLISH_TASK_STATUS_UPDATE),
                    json.dumps({"seq_no": publish_task.seq_no, "status": publish_task.status,
                                "deploy_time": publish_task.deploy_time.strftime("%Y-%m-%d %H:%M:%S"),
                                "deploy_by": publish_task.deploy_by}), 'POST',
                    {'Content-Type': 'application/json'})
    print data
    if data and data.get('code') == -1:
        error = data.get('msg')
        return HttpResponse(error)
    if not data:
        error = u'无法打开目标网址,请联系系统开发人员!'
        return HttpResponse(error)
    return HttpResponseRedirect(reverse('publish_task_list'))


@require_permission('account.perm_can_rollback_publish_task')
def publish_task_rollback(request):
    task_id = request.GET.get('id', '')
    if not task_id:
        return HttpResponseRedirect(reverse('publish_task_list'))
    publish_task = get_object(PublishTask, id=task_id)
    if not publish_task:
        return HttpResponseRedirect(reverse('publish_task_list'))
    publish_task.status = 5
    publish_task.save()
    # 调用接口
    data = api_call('%s%s' % (settings.PUBLISH_CENTER_URL, settings.PUBLISH_TASK_STATUS_UPDATE),
                    json.dumps({"seq_no": publish_task.seq_no, "status": publish_task.status,
                                "deploy_time": publish_task.deploy_time.strftime("%Y-%m-%d %H:%M:%S") if publish_task.deploy_time else '',
                                "deploy_by": publish_task.deploy_by}), 'POST',
                    {'Content-Type': 'application/json'})
    if data and data.get('code') == -1:
        error = data.get('msg')
        return HttpResponse(error)
    if not data:
        error = u'无法打开目标网址,请联系系统开发人员!'
        return HttpResponse(error)
    return HttpResponseRedirect(reverse('publish_task_list'))


def express_app_list(request):
    return render_to_response('index_cu.html', locals(), RequestContext(request))
