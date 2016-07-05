# encoding: utf-8

"""
@version:
@author: liriqiang
@file: views.py
@time: 16-6-2 下午5:29
"""

from django.http import Http404
from django.shortcuts import get_object_or_404
from django.db.models import Q
from django.contrib.auth.decorators import login_required

from account.user_api import *

from account.models import User
from perm.perm_api import get_group_user_perm
from jlog.models import Log


@require_permission('account.perm_can_view_group')
def group_list(request):
    """
    list user group
    用户组列表
    """
    header_title, path1, path2 = '查看用户组', '用户管理', '查看用户组'
    keyword = request.GET.get('search', '')
    user_group_list = Group.objects.all().order_by('name')
    group_id = request.GET.get('id', '')

    if keyword:
        user_group_list = user_group_list.filter(name__icontains=keyword)

    if group_id:
        user_group_list = user_group_list.filter(id=int(group_id))

    user_group_list, p, user_groups, page_range, current_page, show_first, show_end = pages(user_group_list, request)
    return render_to_response('account/group_list.html', locals(), RequestContext(request))


@require_permission('account.perm_can_add_group')
def group_add(request):
    """
    group add view for route
    添加用户组的视图
    """
    error = ''
    msg = ''
    header_title, path1, path2 = '添加用户组', '用户管理', '添加用户组'
    permission_all = Permission.objects.filter(codename__istartswith='perm_').order_by('id')

    if request.method == 'POST':
        group_name = request.POST.get('group_name', '')
        permissions_selected = request.POST.getlist('permissions_selected', '')

        try:
            if not group_name:
                error = u'组名 不能为空'
                raise ServerError(error)

            if Group.objects.filter(name=group_name):
                error = u'组名已存在'
                raise ServerError(error)
            db_add_group(name=group_name, permissions_id=permissions_selected)
        except ServerError:
            pass
        except TypeError:
            error = u'添加小组失败'
        else:
            msg = u'添加组 %s 成功' % group_name

    return render_to_response('account/group_add.html', locals(), RequestContext(request))


@require_permission('account.perm_can_change_group')
def group_edit(request):
    error = ''
    msg = ''
    header_title, path1, path2 = '编辑用户组', '用户管理', '编辑用户组'

    if request.method == 'GET':
        group_id = request.GET.get('id', '')
        user_group = get_object(Group, id=group_id)
        permissions_all = Permission.objects.filter(codename__istartswith='perm_').order_by('id')
        permissions_selected = user_group.permissions.all()
        permissions_remain = list(set(permissions_all) - set(permissions_selected))

    elif request.method == 'POST':
        group_id = request.POST.get('group_id', '')
        group_name = request.POST.get('group_name', '')
        permissions_selected = request.POST.getlist('permissions_selected')

        try:
            if '' in [group_id, group_name]:
                raise ServerError('组名不能为空')

            if len(Group.objects.filter(name=group_name)) > 1:
                raise ServerError(u'%s 用户组已存在' % group_name)
            # add user group
            user_group = get_object_or_404(Group, id=group_id)
            user_group.permissions.clear()

            for permission in Permission.objects.filter(id__in=permissions_selected):
                user_group.permissions.add(permission)

            user_group.name = group_name
            user_group.save()
        except ServerError, e:
            error = e

        if not error:
            return HttpResponseRedirect(reverse('user_group_list'))
        else:
            permissions_all = Permission.objects.filter(codename__istartswith='perm_').order_by('id')
            permissions_selected = user_group.permissions.all()
            permissions_remain = list(set(permissions_all) - set(permissions_selected))

    return render_to_response('account/group_edit.html', locals(), RequestContext(request))


@require_permission('account.perm_can_view_group')
def group_detail(request):
    header_title, path1, path2 = '用户组详情', '用户组管理', '用户组详情'
    group_id = request.GET.get('id', '')
    if not group_id:
        return HttpResponseRedirect(reverse('user_group_list'))
    group = get_object(Group, id=group_id)
    if not group:
        return HttpResponseRedirect(reverse('user_group_list'))
    permissions_all = group.permissions.all()
    user_all = group.user_set.all()
    return render_to_response('account/group_detail.html', locals(), RequestContext(request))


@require_permission('account.perm_can_delete_group')
def group_del(request):
    """
    del a group
    删除用户组
    """
    group_ids = request.GET.get('id', '')
    group_id_list = group_ids.split(',')
    for group_id in group_id_list:
        Group.objects.filter(id=group_id).delete()

    return HttpResponse('删除成功')


@require_permission('account.perm_can_view_user')
def user_list(request):
    header_title, path1, path2 = '查看用户', '用户管理', '用户列表'
    keyword = request.GET.get('keyword', '')
    gid = request.GET.get('gid', '')
    users_list = User.objects.all().order_by('username')

    if gid:
        user_group = Group.objects.filter(id=gid)
        if user_group:
            user_group = user_group[0]
            users_list = user_group.user_set.all()

    if keyword:
        users_list = users_list.filter(Q(username__icontains=keyword) | Q(name__icontains=keyword)).order_by('username')

    users_list, p, users, page_range, current_page, show_first, show_end = pages(users_list, request)

    return render_to_response('account/user_list.html', locals(), RequestContext(request))


@require_permission('account.perm_can_add_user')
def user_add(request):
    error = ''
    msg = ''
    header_title, path1, path2 = '添加用户', '用户管理', '添加用户'
    group_all = Group.objects.all()

    if request.method == 'POST':
        username = request.POST.get('username', '')
        password = PyCrypt.gen_rand_pass(16)
        name = request.POST.get('name', '')
        email = request.POST.get('email', '')
        phone = request.POST.get('phone', '')
        qq = request.POST.get('qq', '')
        groups = request.POST.getlist('groups', [])
        uuid_r = uuid.uuid4().get_hex()
        ssh_key_pwd = PyCrypt.gen_rand_pass(16)
        extra = request.POST.getlist('extra', [])
        is_active = False if '0' in extra else True
        send_mail_need = True if '1' in extra else False

        try:
            if '' in [username, password, ssh_key_pwd, name]:
                error = u'带*内容不能为空'
                raise ServerError
            check_user_is_exist = User.objects.filter(username=username)
            if check_user_is_exist:
                error = u'用户 %s 已存在' % username
                raise ServerError

        except ServerError:
            pass
        else:
            try:
                user = db_add_user(username=username, name=name,
                                   password=password,
                                   email=email, phone=phone, qq=qq,
                                   uuid=uuid_r, groups=groups,
                                   ssh_key_pwd=ssh_key_pwd,
                                   is_active=is_active,
                                   date_joined=datetime.datetime.now())
                server_add_user(username=username, ssh_key_pwd=ssh_key_pwd)
                user = get_object(User, username=username)
                if groups:
                    user_groups = []
                    for user_group_id in groups:
                        user_groups.extend(Group.objects.filter(id=user_group_id))

            except IndexError, e:
                error = u'添加用户 %s 失败 %s ' % (username, e)
                try:
                    db_del_user(username)
                    server_del_user(username)
                except Exception:
                    pass
            else:
                if MAIL_ENABLE and send_mail_need:
                    user_add_mail(user, kwargs=locals())
                msg = get_display_msg(user, password=password, ssh_key_pwd=ssh_key_pwd, send_mail_need=send_mail_need)
    return render_to_response('account/user_add.html', locals(), RequestContext(request))


@require_permission('account.perm_can_change_user')
def user_edit(request):
    header_title, path1, path2 = '编辑用户', '用户管理', '编辑用户'
    if request.method == 'GET':
        user_id = request.GET.get('id', '')
        if not user_id:
            return HttpResponseRedirect(reverse('index'))
        user = get_object(User, id=user_id)
        group_all = Group.objects.all()
        if user:
            groups_str = ' '.join([str(group.id) for group in user.groups.all()])
    else:
        user_id = request.GET.get('id', '')
        password = request.POST.get('password', '')
        name = request.POST.get('name', '')
        email = request.POST.get('email', '')
        phone = request.POST.get('phone', '')
        qq = request.POST.get('qq', '')
        groups = request.POST.getlist('groups', [])
        extra = request.POST.getlist('extra', [])
        is_active = True if '0' in extra else False
        email_need = True if '1' in extra else False

        if user_id:
            user = get_object(User, id=user_id)
        else:
            return HttpResponseRedirect(reverse('user_list'))

        db_update_user(user_id=user_id,
                       password=password,
                       name=name,
                       email=email,
                       phone=phone,
                       qq=qq,
                       groups=groups,
                       is_active=is_active)

        if email_need:
            msg = u"""
            Hi %s:
                您的信息已修改，请登录人人快递网运维平台查看详细信息
                地址：%s
                用户名： %s
                密码：%s (如果密码为None代表密码为原密码)
            """ % (user.name, URL, user.username, password)
            send_mail('您的信息已修改', msg, MAIL_FROM, [email], fail_silently=False)

        return HttpResponseRedirect(reverse('user_list'))
    return render_to_response('account/user_edit.html', locals(), RequestContext(request))


@require_permission('account.perm_can_view_user')
def user_detail(request):
    header_title, path1, path2 = '用户详情', '用户管理', '用户详情'
    user_id = request.GET.get('id', '')
    if not user_id:
        return HttpResponseRedirect(reverse('user_list'))
    user = get_object(User, id=user_id)
    if not user:
        return HttpResponseRedirect(reverse('user_list'))
    user_perm_info = get_group_user_perm(user)
    role_assets = user_perm_info.get('role')
    user_log_ten = Log.objects.filter(user=user.username).order_by('id')[0:10]
    user_log_last = Log.objects.filter(user=user.username).order_by('id')[0:50]
    user_log_last_num = len(user_log_last)

    return render_to_response('account/user_detail.html', locals(), RequestContext(request))


@require_permission('account.perm_can_delete_user')
def user_del(request):
    if request.method == "GET":
        user_ids = request.GET.get('id', '')
        user_id_list = user_ids.split(',')
    elif request.method == "POST":
        user_ids = request.POST.get('id', '')
        user_id_list = user_ids.split(',')
    else:
        return HttpResponse('错误请求')

    for user_id in user_id_list:
        user = get_object(User, id=user_id)
        if user and user.username != 'admin':
            logger.debug(u"删除用户 %s " % user.username)
            server_del_user(user.username)
            user.delete()
    return HttpResponse('删除成功')


def profile(request):
    user_id = request.user.id
    if not user_id:
        return HttpResponseRedirect(reverse('index'))
    user = User.objects.get(id=user_id)
    return render_to_response('account/profile.html', locals(), RequestContext(request))


def change_info(request):
    header_title, path1, path2 = '修改信息', '用户管理', '修改个人信息'
    user_id = request.user.id
    user = User.objects.get(id=user_id)
    error = ''
    if not user:
        return HttpResponseRedirect(reverse('index'))

    if request.method == 'POST':
        name = request.POST.get('name', '')
        password = request.POST.get('password', '')
        email = request.POST.get('email', '')
        phone = request.POST.get('phone', '')
        qq = request.POST.get('qq', '')

        if '' in [name, email]:
            error = '不能为空'

        if not error:
            user.name = name
            user.email = email
            user.phone = phone
            user.qq = qq
            user.save()
            if len(password) > 0:
                user.set_password(password)
                user.save()
            msg = '修改成功'
    return render_to_response('account/change_info.html', locals(), context_instance=RequestContext(request))


@defend_attack
def forget_password(request):
    if request.method == 'POST':
        defend_attack(request)
        email = request.POST.get('email', '')
        username = request.POST.get('username', '')
        name = request.POST.get('name', '')
        user = get_object(User, username=username, email=email, name=name)
        if user:
            timestamp = int(time.time())
            hash_encode = PyCrypt.md5_crypt(str(user.uuid) + str(timestamp) + KEY)
            msg = u"""
            Hi %s, 请点击下面链接重设密码！
            %s/account/password/reset/?uuid=%s&timestamp=%s&hash=%s
            """ % (user.name, URL, user.uuid, timestamp, hash_encode)
            send_mail('忘记跳板机密码', msg, MAIL_FROM, [email], fail_silently=False)
            msg = u'请登陆邮箱，点击邮件重设密码'
            return render_to_response('success.html', locals(), context_instance=RequestContext(request))
        else:
            error = u'用户不存在或邮件地址错误'

    return render_to_response('account/forget_password.html', locals(), context_instance=RequestContext(request))


@defend_attack
def reset_password(request):
    uuid_r = request.GET.get('uuid', '')
    timestamp = request.GET.get('timestamp', '')
    hash_encode = request.GET.get('hash', '')
    action = '/account/password/reset/?uuid=%s&timestamp=%s&hash=%s' % (uuid_r, timestamp, hash_encode)

    if hash_encode == PyCrypt.md5_crypt(uuid_r + timestamp + KEY):
        if int(time.time()) - int(timestamp) > 600:
            return render_to_response('error.html', locals(), context_instance=RequestContext(request))
    else:
        return HttpResponse('hash校验失败')

    if request.method == 'POST':
        password = request.POST.get('password')
        password_confirm = request.POST.get('password_confirm')
        print password, password_confirm
        if password != password_confirm:
            return HttpResponse('密码不匹配')
        else:
            user = get_object(User, uuid=uuid_r)
            if user:
                user.password = PyCrypt.md5_crypt(password)
                user.save()
                return http_success(request, u'密码重设成功')
            else:
                return HttpResponse('用户不存在')

    else:
        return render_to_response('account/reset_password.html', locals(), context_instance=RequestContext(request))


def send_mail_retry(request):
    uuid_r = request.GET.get('uuid', '1')
    user = get_object(User, uuid=uuid_r)
    msg = u"""
    跳板机地址： %s
    用户名：%s
    重设密码：%s/account/password/forget/
    请登录web点击个人信息页面重新生成ssh密钥
    """ % (URL, user.username, URL)

    try:
        send_mail(u'邮件重发', msg, MAIL_FROM, [user.email], fail_silently=False)
    except IndexError:
        return Http404
    return HttpResponse('发送成功')


def regen_ssh_key(request):
    uuid_r = request.GET.get('uuid', '')
    user = get_object(User, uuid=uuid_r)
    if not user:
        return HttpResponse('没有该用户')

    username = user.username
    ssh_key_pass = PyCrypt.gen_rand_pass(16)
    gen_ssh_key(username, ssh_key_pass)
    return HttpResponse('ssh密钥已生成，密码为 %s, 请到下载页面下载' % ssh_key_pass)


@login_required(login_url='/login')
def down_key(request):
    if request.user.is_superuser:
        uuid_r = request.GET.get('uuid', '')
    else:
        user = get_object(User, id=request.user.id)
        uuid_r = user.uuid
    if uuid_r:
        user = get_object(User, uuid=uuid_r)
        if user:
            username = user.username
            private_key_file = os.path.join(KEY_DIR, 'user', username+'.pem')
            if os.path.isfile(private_key_file):
                f = open(private_key_file)
                data = f.read()
                f.close()
                response = HttpResponse(data, content_type='application/octet-stream')
                response['Content-Disposition'] = 'attachment; filename=%s' % os.path.basename(private_key_file)
                if not request.user.is_superuser:
                    os.unlink(private_key_file)
                return response
    return HttpResponse('No Key File. Contact Admin.')
