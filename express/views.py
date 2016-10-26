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
from asset.models import IDC
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
    header_title, path1, path2 = '创建项目', '项目设置', '创建项目'

    yesno_list = list(YES_NO)
    mvnenv_list = list(MVN_ENV)
    languagetype_list = list(LANGUAGE_TYPE)
    idcs = IDC.objects.all()
    idc_list = []
    for idc in idcs:
        idc_list.append(idc.name)

    if request.method == 'POST':
        name = request.POST.get('name', '')
        code = request.POST.get('code', '')
        language_type = request.POST.get('language_type', '')
        git_url = request.POST.get('git_url', '')
        git_branch = request.POST.get('git_branch', '')
        env = request.POST.get('env', '')
        is_full = request.POST.get('is_full', '')
        idc = request.POST.get('idc', '')
        host = request.POST.get('host', '')
        src = request.POST.get('src', '')
        dest = request.POST.get('dest', '')
        tomcat_num = request.POST.get('tomcat_num', '')
        backup_dir = request.POST.get('backup_dir', '')
        ignore_setup = request.POST.get('ignore_setup', '')
        try:
            Project.objects.create(name=name,
                                   code=code,
                                   language_type=language_type,
                                   git_url=git_url,
                                   git_branch=git_branch,
                                   env=env,
                                   is_full=is_full,
                                   idc=idc,
                                   host=host,
                                   src=src,
                                   dest=dest,
                                   tomcat_num=tomcat_num,
                                   backup_dir=backup_dir,
                                   ignore_setup=ignore_setup)
        except ServerError:
            pass
        except Exception as e:
            print e
            error = u'添加项目失败'
        else:
            msg = u'添加项目成功'

    return render_to_response('express/project_add.html', locals(), RequestContext(request))


@require_permission('account.perm_can_edit_project')
def project_edit(request):
    error = ''
    msg = ''
    header_title, path1, path2 = '编辑项目', '项目设置', '编辑项目'

    if request.method == 'GET':
        project_id = request.GET.get('id', '')
        mvnenv_list = list(MVN_ENV)
        yesno_list = list(YES_NO)
        languagetype_list = list(LANGUAGE_TYPE)
        project = get_object(Project, id=project_id)
        idcs = IDC.objects.all()
        idc_list = []
        for idc in idcs:
            idc_list.append(idc.name)

    if request.method == 'POST':
        project_id = request.POST.get('project_id', '')
        name = request.POST.get('name', '')
        code = request.POST.get('code', '')
        language_type = request.POST.get('language_type', '')
        git_url = request.POST.get('git_url', '')
        git_branch = request.POST.get('git_branch', '')
        env = request.POST.get('env', '')
        is_full = request.POST.get('is_full', '')
        idc = request.POST.get('idc', '')
        host = request.POST.get('host', '')
        src = request.POST.get('src', '')
        dest = request.POST.get('dest', '')
        tomcat_num = request.POST.get('tomcat_num', '')
        backup_dir = request.POST.get('backup_dir', '')
        ignore_setup = request.POST.get('ignore_setup', '')
        try:
            Project.objects.filter(id=project_id).update(name=name,
                                                         code=code,
                                                         language_type=language_type,
                                                         git_url=git_url,
                                                         git_branch=git_branch,
                                                         env=env,
                                                         is_full=is_full,
                                                         idc=idc,
                                                         host=host,
                                                         src=src,
                                                         dest=dest,
                                                         tomcat_num=tomcat_num,
                                                         backup_dir=backup_dir,
                                                         ignore_setup=ignore_setup)
        except ServerError:
            pass
        except Exception as e:
            print e
            error = u'保存项目失败'
        else:
            msg = u'保存项目成功'
    return render_to_response('express/project_edit.html', locals(), RequestContext(request))


@require_permission('account.perm_can_view_project')
def project_detail(request):
    header_title, path1, path2 = '查看项目详情', '项目设置', '查看项目详情'
    project_id = request.GET.get('id', '')
    if not project_id:
        return HttpResponseRedirect(reverse('project_list'))
    project = get_object(Project, id=project_id)
    if not project:
        return HttpResponseRedirect(reverse('project_list'))
    return render_to_response('express/project_detail.html', locals(), RequestContext(request))


@require_permission('account.perm_can_delete_project')
def project_del(request):
    """
    del a project
    删除发布任务
    """
    project_ids = request.GET.get('id', '')
    project_id_list = project_ids.split(',')
    for project_id in project_id_list:
        Project.objects.filter(id=project_id).delete()

    return HttpResponse('删除成功')


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
    if request.method == 'POST':
        task_id = request.POST.get('task_id', '')
        if not task_id:
            return HttpResponseRedirect(reverse('publish_task_list'))
        publish_task = get_object(PublishTask, id=task_id)
        if not publish_task:
            return HttpResponseRedirect(reverse('publish_task_list'))
        deploy_type = request.GET.get('deploy_type', '')
        publish_task.is_auto_deploy = 0
        publish_task.idc = deploy_type
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
        return HttpResponseRedirect(reverse('publish_task_list'))
    else:
        task_id = request.GET.get('id', '')
        type_list = []
        if not task_id:
            return HttpResponseRedirect(reverse('publish_task_list'))
        publish_task = get_object(PublishTask, id=task_id)
        if not publish_task:
            return HttpResponseRedirect(reverse('publish_task_list'))
        projects = Project.objects.filter(name=publish_task.project, env=publish_task.env)
        for pro in projects:
            type_list.append(pro.idc)
        print projects
        print type_list
        type_list = list(set(type_list))
        if len(type_list) > 1:
            type_list = [u'全网更新'] + type_list
        else:
            type_list = [u'全网更新']

        host_list = []
        for pro in projects:
            host_list.append(pro.host)

        return render_to_response('express/publish_task_deploy.html', locals(), RequestContext(request))


@require_permission('account.perm_can_deploy_publish_task')
def publish_task_deploy_auto(request):
    task_id = request.GET.get('task_id', '')
    deploy_type = request.GET.get('deploy_type', '')

    if not task_id:
        return HttpResponse('error')
    publish_task = get_object(PublishTask, id=task_id)
    if not publish_task:
        return HttpResponse('error')

    # 只发布模拟环境项目
    if publish_task.env == '1':
        return HttpResponse('sim')

    # 只做php的自动发布
    # projects = Project.objects.filter(name=publish_task.project, env=publish_task.env)
    # print projects[0].language_type
    # if projects[0].language_type != 'PHP':
    #     return HttpResponse('php')

    # 执行发布业务
    is_ok = publish_task_deploy_run(task_id, deploy_type)
    if not is_ok:
        return HttpResponse('error')

    # 更新任务状态
    publish_task.is_auto_deploy = 1
    publish_task.idc = deploy_type
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
        print error
        return HttpResponse('error')

    # 更新项目信息
    if deploy_type == u'全网更新':
        projects = Project.objects.filter(name=publish_task.project, env=publish_task.env)
    else:
        projects = Project.objects.filter(name=publish_task.project, env=publish_task.env, idc=deploy_type)
    for project in projects:
        project.git_branch = publish_task.code_tag
        project.save()

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

    # 回滚线上备份代码
    # 判断是否是自动发布
    print publish_task.is_auto_deploy
    if publish_task.is_auto_deploy == '1':
        if not publish_task_rollback_run(publish_task):
            return HttpResponse('error')

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
