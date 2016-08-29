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
from express_api import *
from account.models import User


@require_permission('account.perm_can_view_project')
def project_list(request):
    """
    项目列表
    :param request:
    :return:
    """
    header_title, path1, path2 = '查看项目信息', '发布任务管理', '查看项目信息'
    keyword = request.GET.get('keyword', '')
    project_list = Project.objects.all()
    task_id = request.GET.get('id', '')

    if task_id:
        project_list = project_list.filter(id=task_id)

    if keyword:
        project_list = project_list.filter(name__icontains=keyword)

    project_list, p, projects, page_range, current_page, show_first, show_end = pages(project_list, request)
    return render_to_response('express/project_list.html', locals(), RequestContext(request))


@require_permission('account.perm_can_add_project')
def project_add(request):
    """
    project add view for route
    添加 项目信息 的视图
    """
    error = ''
    msg = ''
    header_title, path1, path2 = '创建发布任务', '发布任务管理', '创建发布任务'

    yesno_list = list(YES_NO)
    env_list = list(ENV)

    if request.method == 'POST':
        product = request.POST.get('product', '')
        project = request.POST.get('project', '')
        env = request.POST.get('env', '')
        version = request.POST.get('version', '')
        update_remark = request.POST.get('update_remark', '')
        code_dir = request.POST.get('code_dir', '')
        code_tag = request.POST.get('code_tag', '')
        database_update = request.POST.get('database_update', '')
        settings = request.POST.get('settings', '')
        update_note = request.POST.get('update_note', '')
        owner = request.POST.get('owner', '')
        try:
            create_time = timezone.now()
            PublishTask.objects.create(seq_no=seq_no,
                                       product=product,
                                       project=project,
                                       env=env,
                                       version=version,
                                       update_remark=update_remark,
                                       code_dir=code_dir,
                                       code_tag=code_tag,
                                       database_update=database_update,
                                       upload_sql=upload_sql_name,
                                       settings=settings,
                                       update_note=update_note,
                                       owner=owner,
                                       create_time=create_time,
                                       create_by=request.user.username,
                                       status=1)
        except ServerError:
            pass
        except Exception as e:
            print e
            error = u'添加任务失败'
        else:
            msg = u'添加任务成功'

    return render_to_response('express/project_add.html', locals(), RequestContext(request))


@require_permission('account.perm_can_edit_project')
def project_edit(request):
    pass


@require_permission('account.perm_can_view_project')
def project_detail(request):
    pass


@require_permission('account.perm_can_delete_project')
def project_del(request):
    pass


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
    publish_task.deploy_time = timezone.now()
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

    # 执行发布业务

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
        print error
        return HttpResponse('error')
    if not data:
        error = u'无法打开目标网址,请联系系统开发人员!'
        print error
        return HttpResponse('error')
    return HttpResponseRedirect(reverse('publish_task_list'))


@require_permission('account.perm_can_view_app_publish_task')
def app_publish_task_list(request):
    """
    list app publish task
    发布任务列表
    """
    header_title, path1, path2 = '查看APP更新任务', '发布任务管理', '查看APP更新任务'
    keyword = request.GET.get('search', '')
    app_publish_task_list = AppPublishTask.objects.all().order_by('-seq_no')
    task_id = request.GET.get('id', '')

    if keyword:
        app_publish_task_list = app_publish_task_list.filter(name__icontains=keyword)

    if task_id:
        app_publish_task_list = app_publish_task_list.filter(id=int(task_id))

    app_publish_task_list, p, app_publish_tasks, page_range, current_page, show_first, show_end = pages(app_publish_task_list, request)
    return render_to_response('express/app_publish_task_list.html', locals(), RequestContext(request))


@require_permission('account.perm_can_view_app_publish_task')
def app_publish_task_detail(request):
    header_title, path1, path2 = 'APP发布任务详情', '发布任务管理', 'APP发布任务详情'
    task_id = request.GET.get('id', '')
    if not task_id:
        return HttpResponseRedirect(reverse('app_publish_task_list'))
    app_publish_task = get_object(AppPublishTask, id=task_id)
    if not app_publish_task:
        return HttpResponseRedirect(reverse('app_publish_task_list'))
    return render_to_response('express/app_publish_task_detail.html', locals(), RequestContext(request))


@require_permission('account.perm_can_trash_app_publish_task')
def app_publish_task_trash(request):
    task_id = request.GET.get('id', '')
    if not task_id:
        return HttpResponseRedirect(reverse('app_publish_task_list'))
    app_publish_task = get_object(AppPublishTask, id=task_id)
    if not app_publish_task:
        return HttpResponseRedirect(reverse('app_publish_task_list'))
    app_publish_task.status = 6
    app_publish_task.save()
    # 调用接口
    data = api_call('%s%s' % (settings.PUBLISH_CENTER_URL, settings.APP_PUBLISH_TASK_STATUS_UPDATE),
                    json.dumps({"seq_no": app_publish_task.seq_no, "status": app_publish_task.status,
                                "deploy_time": app_publish_task.deploy_time.strftime("%Y-%m-%d %H:%M:%S") if app_publish_task.deploy_time else '',
                                "deploy_by": app_publish_task.deploy_by}), 'POST',
                    {'Content-Type': 'application/json'})
    if data and data.get('code') == -1:
        error = data.get('msg')
        print error
        return HttpResponse('error')
    if not data:
        error = u'无法打开目标网址,请联系系统开发人员!'
        print error
        return HttpResponse('error')
    return HttpResponseRedirect(reverse('app_publish_task_list'))


@require_permission('account.perm_can_deploy_app_publish_task')
def app_publish_task_deploy(request):
    task_id = request.GET.get('id', '')
    if not task_id:
        return HttpResponseRedirect(reverse('app_publish_task_list'))
    app_publish_task = get_object(AppPublishTask, id=task_id)
    if not app_publish_task:
        return HttpResponseRedirect(reverse('app_publish_task_list'))
    # 执行异步发布任务
    app_publish_task_express(task_id)
    app_publish_task.status = 4
    app_publish_task.deploy_time = timezone.now()
    app_publish_task.deploy_by = request.user.username
    app_publish_task.save()
    # 调用接口
    data = api_call('%s%s' % (settings.PUBLISH_CENTER_URL, settings.APP_PUBLISH_TASK_STATUS_UPDATE),
                    json.dumps({"seq_no": app_publish_task.seq_no, "status": app_publish_task.status,
                                "deploy_time": app_publish_task.deploy_time.strftime("%Y-%m-%d %H:%M:%S"),
                                "deploy_by": app_publish_task.deploy_by}), 'POST',
                    {'Content-Type': 'application/json'})
    if data and data.get('code') == -1:
        error = data.get('msg')
        print error
        return HttpResponse('error')
    if not data:
        error = u'无法打开目标网址,请联系系统开发人员!'
        print error
        return HttpResponse('error')
    return HttpResponseRedirect(reverse('app_publish_task_list'))


@require_permission('account.perm_can_rollback_app_publish_task')
def app_publish_task_rollback(request):
    task_id = request.GET.get('id', '')
    if not task_id:
        return HttpResponseRedirect(reverse('app_publish_task_list'))
    app_publish_task = get_object(AppPublishTask, id=task_id)
    if not app_publish_task:
        return HttpResponseRedirect(reverse('app_publish_task_list'))
    app_publish_task_rollback_config(task_id)
    app_publish_task.status = 5
    app_publish_task.save()
    # 调用接口
    data = api_call('%s%s' % (settings.PUBLISH_CENTER_URL, settings.APP_PUBLISH_TASK_STATUS_UPDATE),
                    json.dumps({"seq_no": app_publish_task.seq_no, "status": app_publish_task.status,
                                "deploy_time": app_publish_task.deploy_time.strftime("%Y-%m-%d %H:%M:%S") if app_publish_task.deploy_time else '',
                                "deploy_by": app_publish_task.deploy_by}), 'POST',
                    {'Content-Type': 'application/json'})
    if data and data.get('code') == -1:
        error = data.get('msg')
        return HttpResponse(error)
    if not data:
        error = u'无法打开目标网址,请联系系统开发人员!'
        return HttpResponse(error)
    return HttpResponseRedirect(reverse('app_publish_task_list'))
