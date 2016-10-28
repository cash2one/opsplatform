# encoding: utf-8

"""
@version:
@author: liriqiang
@file: views.py
@time: 16-6-2 下午5:10
"""
from django.shortcuts import render
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.db.models import Count
from account.models import User
from asset.models import Asset
from perm.perm_api import get_group_user_perm, gen_resource
from perm.ansible_api import MyRunner
from jlog.models import Log, FileLog
from api import *
import zipfile
from qiniu import Auth, put_data, etag


def getDaysByNum(num):
    """
    输出格式:([datetime.date(2015, 11, 6),  datetime.date(2015, 11, 8)], ['11-06', '11-08'])
    """

    today = datetime.date.today()
    oneday = datetime.timedelta(days=1)
    date_li, date_str = [], []
    for i in range(0, num):
        today = today-oneday
        date_li.append(today)
        date_str.append(str(today)[5:10])
    date_li.reverse()
    date_str.reverse()
    return date_li, date_str


def get_data(x, y, z):
    pass


def get_data_by_day(date_li, item):
    data_li = []
    for d in date_li:
        logs = Log.objects.filter(start_time__year=d.year,
                                  start_time__month=d.month,
                                  start_time__day=d.day)
        if item == 'user':
            data_li.append(set([log.user for log in logs]))
        elif item == 'asset':
            data_li.append(set([log.host for log in logs]))
        elif item == 'login':
            data_li.append(logs)
        else:
            pass
    return data_li


def get_count_by_day(date_li, item):
    data_li = get_data_by_day(date_li, item)
    data_count_li = []
    for data in data_li:
        data_count_li.append(len(data))
    return data_count_li


def get_count_by_date(date_li, item):
    data_li = get_data_by_day(date_li, item)
    data_count_tmp = []
    for data in data_li:
        data_count_tmp.extend(list(data))

    return len(set(data_count_tmp))


@login_required(login_url="login/")
def index(request):
    li_date, li_str = getDaysByNum(7)
    today = datetime.datetime.now().day
    from_week = datetime.datetime.now() - datetime.timedelta(days=7)

    if not request.user.has_perm('perm_can_view_dashboard'):
        user = request.user
        # 最后10次登陆
        login_10 = Log.objects.filter(user=user.username).order_by('-start_time')[:10]
        login_more_10 = Log.objects.filter(user=user.username).order_by('-start_time')[10:]
        return render_to_response('index_cu.html', locals(), context_instance=RequestContext(request))

    else:
        # dashboard 显示汇总
        users = User.objects.all()
        hosts = Asset.objects.all()
        online = Log.objects.filter(is_finished=0)
        online_host = online.values('host').distinct()
        online_user = online.values('user').distinct()
        active_users = User.objects.filter(is_active=1)
        active_hosts = Asset.objects.filter(is_active=1)

        # 一个月历史汇总
        date_li, date_str = getDaysByNum(30)
        date_month = repr(date_str)
        active_user_per_month = str(get_count_by_day(date_li, 'user'))
        active_asset_per_month = str(get_count_by_day(date_li, 'asset'))
        active_login_per_month = str(get_count_by_day(date_li, 'login'))

        # 活跃用户资产图
        active_user_month = get_count_by_date(date_li, 'user')
        disabled_user_count = len(users.filter(is_active=False))
        inactive_user_month = len(users) - active_user_month
        active_asset_month = get_count_by_date(date_li, 'asset')
        disabled_asset_count = len(hosts.filter(is_active=False)) if hosts.filter(is_active=False) else 0
        inactive_asset_month = len(hosts) - active_asset_month if len(hosts) > active_asset_month else 0

        # 一周top10用户和主机
        week_data = Log.objects.filter(start_time__range=[from_week, datetime.datetime.now()])
        user_top_ten = week_data.values('user').annotate(times=Count('user')).order_by('-times')[:10]
        host_top_ten = week_data.values('host').annotate(times=Count('host')).order_by('-times')[:10]

        for user_info in user_top_ten:
            username = user_info.get('user')
            last = Log.objects.filter(user=username).latest('start_time')
            user_info['last'] = last

        for host_info in host_top_ten:
            host = host_info.get('host')
            last = Log.objects.filter(host=host).latest('start_time')
            host_info['last'] = last

        # 一周top5
        week_users = week_data.values('user').distinct().count()
        week_hosts = week_data.count()

        user_top_five = week_data.values('user').annotate(times=Count('user')).order_by('-times')[:5]
        color = ['label-success', 'label-info', 'label-primary', 'label-default', 'label-warnning']

        # 最后10次权限申请
        # perm apply latest 10
        # perm_apply_10 = Apply.objects.order_by('-date_add')[:10]

        # 最后10次登陆
        login_10 = Log.objects.order_by('-start_time')[:10]
        login_more_10 = Log.objects.order_by('-start_time')[10:21]

    return render_to_response('index.html', locals(), context_instance=RequestContext(request))


def skin_config(request):
    return render_to_response('skin_config.html')


@defend_attack
def Login(request):
    """登录界面"""
    error = ''
    if request.user.is_authenticated():
        return HttpResponseRedirect(reverse('index'))
    if request.method == 'GET':
        return render(request, 'login.html')
    else:
        username = request.POST.get('username')
        password = request.POST.get('password')
        if username and password:
            user = authenticate(username=username, password=password)
            if user is not None:
                if user.is_active:
                    login(request, user)
                    response = HttpResponseRedirect(request.session.get('pre_url', '/'))
                    response.set_cookie('sig', request.session.session_key, expires=604800)
                    return response
                else:
                    error = '用户未激活'
            else:
                error = '用户名或密码错误'
        else:
            error = '用户名或密码错误'
    return render(request, 'login.html', {'error': error})


def Logout(request):
    logout(request)
    return HttpResponseRedirect(reverse('index'))


@login_required(login_url='/login')
def upload(request):
    user = request.user
    assets = get_group_user_perm(user).get('asset').keys()
    asset_select = []
    if request.method == 'POST':
        remote_ip = request.META.get('REMOTE_ADDR')
        asset_ids = request.POST.getlist('asset_ids', '')
        upload_files = request.FILES.getlist('file[]', None)
        date_now = datetime.datetime.now().strftime("%Y%m%d%H%M%S")
        upload_dir = get_tmp_dir()
        # file_dict = {}
        for asset_id in asset_ids:
            asset_select.append(get_object(Asset, id=asset_id))

        if not set(asset_select).issubset(set(assets)):
            illegal_asset = set(asset_select).issubset(set(assets))
            return HttpResponse('没有权限的服务器 %s' % ','.join([asset.hostname for asset in illegal_asset]))

        for upload_file in upload_files:
            file_path = '%s/%s' % (upload_dir, upload_file.name)
            with open(file_path, 'w') as f:
                for chunk in upload_file.chunks():
                    f.write(chunk)

        res = gen_resource({'user': user, 'asset': asset_select})
        runner = MyRunner(res)
        runner.run('copy', module_args='src=%s dest=%s directory_mode'
                                        % (upload_dir, '/tmp'), pattern='*')
        ret = runner.results
        logger.debug(ret)
        FileLog(user=request.user.username, host=' '.join([asset.hostname for asset in asset_select]),
                filename=' '.join([f.name for f in upload_files]), type='upload', remote_ip=remote_ip,
                result=ret).save()
        if ret.get('failed'):
            error = u'上传目录: %s <br> 上传失败: [ %s ] <br>上传成功 [ %s ]' % (upload_dir,
                                                                             ', '.join(ret.get('failed').keys()),
                                                                             ', '.join(ret.get('ok').keys()))
            return HttpResponse(error, status=500)
        msg = u'上传目录: %s <br> 传送成功 [ %s ]' % (upload_dir, ', '.join(ret.get('ok').keys()))
        return HttpResponse(msg)
    return render_to_response('upload.html', locals(), RequestContext(request))


@login_required(login_url='/login')
def download(request):
    user = request.user
    assets = get_group_user_perm(user).get('asset').keys()
    asset_select = []
    if request.method == 'POST':
        remote_ip = request.META.get('REMOTE_ADDR')
        asset_ids = request.POST.getlist('asset_ids', '')
        file_path = request.POST.get('file_path')
        date_now = datetime.datetime.now().strftime("%Y%m%d%H%M%S")
        upload_dir = get_tmp_dir()
        for asset_id in asset_ids:
            asset_select.append(get_object(Asset, id=asset_id))

        if not set(asset_select).issubset(set(assets)):
            illegal_asset = set(asset_select).issubset(set(assets))
            return HttpResponse(u'没有权限的服务器 %s' % ','.join([asset.hostname for asset in illegal_asset]))

        res = gen_resource({'user': user, 'asset': asset_select})
        runner = MyRunner(res)
        runner.run('fetch', module_args='src=%s dest=%s' % (file_path, upload_dir), pattern='*')
        FileLog(user=request.user.username, host=' '.join([asset.hostname for asset in asset_select]),
                filename=file_path, type='download', remote_ip=remote_ip, result=runner.results).save()
        logger.debug(runner.results)
        tmp_dir_name = os.path.basename(upload_dir)
        file_zip = '/tmp/'+tmp_dir_name+'.zip'
        zf = zipfile.ZipFile(file_zip, "w", zipfile.ZIP_DEFLATED)
        for dirname, subdirs, files in os.walk(upload_dir):
            zf.write(dirname)
            for filename in files:
                zf.write(os.path.join(dirname, filename))
        zf.close()
        f = open(file_zip)
        data = f.read()
        f.close()
        response = HttpResponse(data, content_type='application/octet-stream')
        response['Content-Disposition'] = 'attachment; filename=%s.zip' % tmp_dir_name
        return response

    return render_to_response('download.html', locals(), context_instance=RequestContext(request))


@login_required(login_url='/login')
def exec_cmd(request):
    role = request.GET.get('role')
    check_assets = request.GET.get('check_assets', '')
    web_terminal_uri = '/ws/exec?role=%s' % role
    return render(request, 'exec_cmd.html', locals())


@login_required(login_url='/login')
def web_terminal(request):
    asset_id = request.GET.get('id')
    role_name = request.GET.get('role')
    asset = get_object(Asset, id=asset_id)
    if asset:
        hostname = asset.hostname
    return render_to_response('web_terminal.html', locals())


@login_required(login_url='/login')
def qiniu_portal(request):
    error = ''
    msg = ''
    if request.method == 'POST':
        bucket = request.POST.get('bucket')
        upload_name = request.POST.get('upload_name')
        if request.FILES:
            upload_file = request.FILES['upload_file']
        else:
            return HttpResponse('error')

        access_key = QINIU_ACCESS_KEY
        secret_key = QINIU_SECRET_KEY

        q = Auth(access_key, secret_key)

        bucket_name = 'lrqrun'

        key = upload_name

        token = q.upload_token(bucket_name, key, 3600)

        data = upload_file

        ret, info = put_data(token, key, data)

        print(info)

        assert ret['key'] == key
        msg = '上传成功'
        return render_to_response('qiniu_portal.html', locals(), context_instance=RequestContext(request))
    return render_to_response('qiniu_portal.html', locals(), context_instance=RequestContext(request))
