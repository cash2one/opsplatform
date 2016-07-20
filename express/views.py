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


def express_list(request):
    """
    list user group
    用户组列表
    """
    header_title, path1, path2 = '查看发布任务', '代码发布', '查看发布任务'
    keyword = request.GET.get('search', '')
    publish_task_list = PublishTask.objects.all().order_by('seq_no')
    publish_task_id = request.GET.get('id', '')

    if keyword:
        publish_task_list = publish_task_list.filter(seq_no__icontains=keyword)

    if publish_task_id:
        publish_task_list = publish_task_list.filter(id=int(publish_task_id))

    publish_task_list, p, publish_tasks, page_range, current_page, show_first, show_end = pages(publish_task_list, request)
    return render_to_response('express/express_list.html', locals(), RequestContext(request))


def express_add(request):
    """
    group add view for route
    添加用户组的视图
    """
    error = ''
    msg = ''
    header_title, path1, path2 = '添加发布任务', '代码发布', '添加发布任务'

    if request.method == 'POST':
        product = request.POST.get('product', '')
        project = request.POST.get('project', '')
        type = request.POST.get('type', '')
        version = request.POST.get('version', '')
        update_remark = request.POST.get('update_remark', '')
        code_dir = request.POST.get('code_dir', '')
        settings = request.POST.get('settings', '')
        update_note = request.POST.get('update_note', '')
        owner = request.POST.get('owner', '')
        try:
            current_year = timezone.now().year
            current_month = timezone.now().month
            current_day = timezone.now().day
            latest = PublishTask.objects.filter(submit_time__startswith=
                                                  datetime.date(current_year,
                                                                current_month,
                                                                current_day)).order_by('-seq_no')
            if latest:
                latest = latest[0]
                num = int(latest.seq_no[-2:]) + 1
            else:
                num = 1
            seq_no = 'RRPS-%s%s%s%s' % (current_year, '%02i' % current_month, '%02i' % current_day, '%02i' % num)
            submit_time = datetime.datetime.now()
            print submit_time
            PublishTask.objects.create(seq_no=seq_no,
                                       product=product,
                                       project=project,
                                       type=type,
                                       version=version,
                                       update_remark=update_remark,
                                       code_dir=code_dir,
                                       settings=settings,
                                       update_note=update_note,
                                       owner=owner,
                                       submit_time=submit_time,
                                       submit_by=request.user.username,
                                       status='pending')
        except ServerError:
            pass
        except TypeError:
            error = u'添加任务失败'
        else:
            msg = u'添加任务 %s 成功' % seq_no

    return render_to_response('express/express_add.html', locals(), RequestContext(request))


def express_detail(request):
    pass


def express_app_list(request):
    return render_to_response('index_cu.html', locals(), RequestContext(request))
