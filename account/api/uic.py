# encoding: utf-8

"""
@version: 
@author: liriqiang
@file: uic.py
@time: 16-6-16 下午4:13
"""
from opsplatform.api import *
from account.models import User
from django.contrib.sessions.models import Session
from django.contrib.auth.models import Group


def sso_sig(request):
    """
     获取随机UUID
    """
    return HttpResponse(uuid.uuid4().get_hex())


def sso_user(request, sig=''):
    """
    根据UUID数据获取用户数据
    """
    if not sig:
        return HttpResponse('sig is blank')
    session = Session.objects.get(session_key=sig)
    uid = session.get_decoded().get('_auth_user_id')
    user = User.objects.get(pk=uid)
    if not user:
        return HttpResponse('no such user')
    u = {
        "id": user.id,
        "name": user.username,
        "cnname": user.name,
        "email": user.email,
        "phone": user.phone,
        "im": user.qq,
        "qq": user.qq,
        "role": user.is_superuser
    }
    return JsonResponse({'user': u})


def auth_login(request):
    session_key = request.GET.get('sig', '')
    callback = request.GET.get('callback', '')
    if request.COOKIES.get('sig'):
        cookie_session_key = request.COOKIES.get('sig')
    else:
        cookie_session_key = request.get_argument('sig', '')
    if cookie_session_key == "":
        request.session['pre_url'] = callback
        return HttpResponseRedirect(reverse('login'))
    session = get_object(Session, session_key=cookie_session_key)
    if session and datetime.datetime.now() < session.expire_date:
        return HttpResponseRedirect(callback)
    if session_key and callback:
        request.session['pre_url'] = callback
        return HttpResponseRedirect(reverse('login'))
    else:
        return HttpResponseRedirect(reverse('login'))


def team_query(request):
    query = request.GET.get('query', '')
    limit = request.GET.get('limit', 10)
    groups = Group.objects.filter(name__contains=query)[:limit]
    teams = []
    for group in groups:
        team = {
            "id": group.id,
            "name": group.name,
            "resume": group.name,
            "creator": ""
        }
        teams.append(team)
    return JsonResponse({"msg": "", "teams": teams})


def team_users(request):
    name = request.GET.get('name', '')
    group = get_object(Group, name=name)
    users = []
    if group:
        users_obj = User.objects.filter(groups=group)
        for user_obj in users_obj:
            user = {
                "id": user_obj.id,
                "name": user_obj.username,
                "cnname": user_obj.name,
                "email": user_obj.email,
                "phone": user_obj.phone,
                "im": user_obj.qq,
                "qq": user_obj.qq,
                "role": user_obj.is_superuser
            }
            users.append(user)

    return JsonResponse({"msg": "", "users": users})


def team_all(request):
    return HttpResponseRedirect(reverse('user_group_list'))


def user_in(request):
    name = request.GET.get('name', '')
    teams = request.GET.get('teams', '')
    groups = teams.split(',')
    for group in groups:
        team = get_object(Group, name=group)
        if team:
            users_obj = User.objects.filter(groups=team)
            for user_obj in users_obj:
                if user_obj.username == name:
                    return HttpResponse('1')

    return HttpResponse('0')


def about_user(request, user):
    if not user:
        return HttpResponseRedirect(reverse('index'))
    user = User.objects.get(username=user)
    return render_to_response('account/profile.html', locals(), RequestContext(request))
