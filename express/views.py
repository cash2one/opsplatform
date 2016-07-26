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


def publish_task_list(request):
    """
    list publish task
    发布任务列表
    """
    header_title, path1, path2 = '查看发布任务', '发布任务管理', '查看发布任务'
    keyword = request.GET.get('search', '')
    publish_task_list = PublishTask.objects.all().order_by('-seq_no')
    task_id = request.GET.get('id', '')

    if keyword:
        publish_task_list = publish_task_list.filter(name__icontains=keyword)

    if task_id:
        publish_task_list = publish_task_list.filter(id=int(task_id))

    publish_task_list, p, publish_tasks, page_range, current_page, show_first, show_end = pages(publish_task_list, request)
    return render_to_response('express/publish_task_list.html', locals(), RequestContext(request))


def publish_task_detail(request):
    header_title, path1, path2 = '发布任务详情', '查看发布任务', '发布任务详情'
    task_id = request.GET.get('id', '')
    if not task_id:
        return HttpResponseRedirect(reverse('publish_task_list'))
    publish_task = get_object(PublishTask, id=task_id)
    if not publish_task:
        return HttpResponseRedirect(reverse('publish_task_list'))
    return render_to_response('express/publish_task_detail.html', locals(), RequestContext(request))


def publish_task_trash(request):
    pass


def publish_task_deploy(request):
    pass


def publish_task_rollback(request):
    pass


def express_app_list(request):
    return render_to_response('index_cu.html', locals(), RequestContext(request))
