from opsplatform.api import *
from models import *


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
    return HttpResponse('none')


@require_permission('account.perm_can_delete_note')
def note_del(request):
    return HttpResponse('none')
