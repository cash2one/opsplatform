# encoding: utf-8

"""
@version:
@author: liriqiang
@file: urls.py
@time: 16-7-11 下午5:51
"""

from opsplatform.api import *
from models import *
from opsplatform import settings
from account.models import *
from django.contrib.auth.models import Group
from opsplatform.send import sms_send


@require_permission('account.perm_can_view_note')
def note_list(request):
    keyword = request.GET.get('search', '')
    notes_list = Note.objects.all().order_by('create_at')
    note_id = request.GET.get('id', '')
    if keyword:
        notes_list = notes_list.filter(text__icontains=keyword)

    if note_id:
        notes_list = notes_list.filter(id=int(note_id))

    notes_list, p, notes, page_range, current_page, show_first, show_end = pages(notes_list, request)
    return render_to_response('note/note_list.html', locals(), RequestContext(request))


@require_permission('account.perm_can_add_note')
def note_add(request):

    error = ''
    msg = ''

    if request.method == 'POST':
        note_text = request.POST.get('note_text', '')

        try:
            if not note_text:
                error = u'记录 不能为空'
                raise ServerError(error)
            Note.objects.create(text=note_text, create_by=request.user.username)
            msg = u"""
                Hi All,
                    运维平台有新的运维记录新增

                    %s
            """ % note_text
            group = get_object(Group, name='运维组')
            users_obj = User.objects.filter(groups=group)
            sa_email = []
            sa_sms = []
            for user_obj in users_obj:
                sa_email.append(user_obj.email) if user_obj.email else None
                sa_sms.append(user_obj.phone) if user_obj.phone else None
            send_mail('[运维平台][运维记录提醒]', msg, settings.EMAIL_HOST_USER, sa_email, fail_silently=False)
            sms_msg = u"""【运维平台】%s""" % note_text
            sms_send(sa_sms, sms_msg)
        except ServerError:
            pass
        except TypeError:
            error = u'添加记录失败'
        else:
            msg = u'添加记录成功'

    return render_to_response('note/note_add.html', locals(), RequestContext(request))


@require_permission('account.perm_can_change_note')
def note_edit(request):

    error = ''
    msg = ''

    if request.method == 'GET':
        note_id = request.GET.get('id', '')
        note = get_object(Note, id=note_id)

    elif request.method == 'POST':
        note_id = request.POST.get('note_id', '')
        note_text = request.POST.get('note_text', '')

        try:
            if '' in [note_id, note_text]:
                raise ServerError('记录不能为空')
            note_object = get_object(Note, id=note_id)
            note_object.text = note_text
            note_object.save()
        except ServerError, e:
            error = e

        if not error:
            return HttpResponseRedirect(reverse('note_list'))

    return render_to_response('note/note_edit.html', locals(), RequestContext(request))


@require_permission('account.perm_can_delete_note')
def note_del(request):
    note_ids = request.GET.get('id', '')
    note_id_list = note_ids.split(',')
    for note_id in note_id_list:
        Note.objects.filter(id=note_id).delete()

    return HttpResponse('删除成功')
