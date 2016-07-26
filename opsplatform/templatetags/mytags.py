# encoding: utf-8

"""
@version: 
@author: liriqiang
@file: mytags.py
@time: 16-6-2 下午7:00
"""
import ast

from django import template
from opsplatform.api import *

from account.models import User
from django.contrib.auth.models import Group, Permission
from monitor.models import DashboardScreen
from express.models import *
from perm.perm_api import get_group_user_perm

register = template.Library()


@register.filter(name='int2str')
def int2str(value):
    """
    int 转换为 str
    """
    return str(value)


@register.filter(name='bool2str')
def bool2str(value):
    if value:
        return u'是'
    else:
        return u'否'


@register.filter(name='none2null')
def none2null(value):
    if value:
        return value
    else:
        return u''


@register.filter(name='groups2str')
def groups2str(group_list):
    """
    将用户组列表转换为str
    """
    if len(group_list) < 3:
        return ' | '.join([group.name for group in group_list])
    else:
        return '%s ...' % ' '.join([group.name for group in group_list[0:2]])


@register.filter(name='group_str2')
def groups_str2(group_list):
    """
    将用户组列表转换为str
    """
    if len(group_list) < 3:
        return ' '.join([group.name for group in group_list])
    else:
        return '%s ...' % ' '.join([group.name for group in group_list[0:2]])


@register.filter(name='str_to_list')
def str_to_list(info):
    """
    str to list
    """
    print ast.literal_eval(info), type(ast.literal_eval(info))
    return ast.literal_eval(info)


@register.filter(name='str_to_dic')
def str_to_dic(info):
    """
    str to list
    """
    if '{' in info:
        info_dic = ast.literal_eval(info).iteritems()
    else:
        info_dic = {}
    return info_dic


@register.filter(name='str_to_code')
def str_to_code(char_str):
    if char_str:
        return char_str
    else:
        return u'空'


@register.filter(name='ip_str_to_list')
def ip_str_to_list(ip_str):
    """
    ip str to list
    """
    return ip_str.split(',')


@register.filter(name='to_avatar')
def to_avatar(username=0):
    """不同角色不同头像"""
    role_id = 0
    role_dict = {'0': 'user', '1': 'admin', '2': 'root'}
    user = get_object(User, username=username)
    if user:
        if user.is_superuser:
            role_id = 2
        elif 'Admin' in user.groups.all():
            role_id = 1
        else:
            role_id = 0
    return role_dict.get(str(role_id), 'user')


@register.filter(name='members_count')
def members_count(group_id):
    """统计用户组下成员数量"""
    group = get_object(Group, id=group_id)
    if group:
        return group.user_set.count()
    else:
        return 0


@register.filter(name='get_permission_name')
def get_permission_name(permission_id):
    """ 根据权限ID获取权限名"""
    permission = get_object(Permission, id=permission_id)
    if permission:
        return unicode(permission.name)
    else:
        return u''


@register.filter(name='get_role')
def get_role(user_id):
    """
    根据用户id获取用户权限
    """
    print user_id
    user = get_object(User, id=user_id)
    if user:
        if user.is_superuser:
            return u'超级系统管理员'
        groups = user.groups.all()
        group_name = []
        for group in groups:
            group_name.append(unicode(group.name))
        if group_name:
            return u' | '.join(group_name)
        else:
            return u"普通用户"
    else:
        return u"[异常用户]"


@register.filter(name='user_asset_count')
def user_asset_count(user):
    """
    返回用户权限主机的数量
    """
    assets = user.asset.all()
    asset_groups = user.asset_group.all()

    for asset_group in asset_groups:
        if asset_group:
            assets.extend(asset_group.asset_set.all())

    return len(assets)


@register.filter(name='user_perm_asset_num')
def user_perm_asset_num(user_id):
    user = get_object(User, id=user_id)
    if user:
        user_perm_info = get_group_user_perm(user)
        return len(user_perm_info.get('asset').keys())
    else:
        return 0


@register.filter(name='key_exist')
def key_exist(username):
    """
    ssh key is exist or not
    """
    if os.path.isfile(os.path.join(KEY_DIR, 'user', username+'.pem')):
        return True
    else:
        return False


@register.filter(name='rule_member_count')
def rule_member_count(instance, member):
    """
    instance is a rule object,
    use to get the number of the members
    :param instance:
    :param member:
    :return:
    """
    member = getattr(instance, member)
    counts = member.all().count()
    return str(counts)


@register.filter(name='role_contain_which_sudos')
def role_contain_which_sudos(role):
    """
    get role sudo commands
    """
    sudo_names = [sudo.name for sudo in role.sudo.all()]
    return ','.join(sudo_names)


@register.filter(name='get_cpu_core')
def get_cpu_core(cpu_info):
    cpu_core = cpu_info.split('* ')[1] if cpu_info and '*' in cpu_info else cpu_info
    return cpu_core


@register.filter(name='get_disk_info')
def get_disk_info(disk_info):
    try:
        disk_size = 0
        if disk_info:
            disk_dic = ast.literal_eval(disk_info)
            for disk, size in disk_dic.items():
                disk_size += size
            disk_size = int(disk_size)
        else:
            disk_size = ''
    except Exception:
        disk_size = disk_info
    return disk_size


@register.filter(name='i_cols')
def i_cols(i, cols):
    return int(i) % int(cols) == 0


@register.filter(name='cols_12int')
def cols_12int(cols):
    return int(12/int(cols))


@register.filter(name='big_graph')
def big_graph(src):
    return src.replace("graph_type=h", "").replace("graph_type=k", "").replace("graph_type=a", "")


@register.filter(name='find_graph_h')
def find_graph_h(big_src):
    return big_src.find("/chart/h")


@register.filter(name='find_graph_k')
def find_graph_k(big_src):
    return big_src.find("/chart/k")


@register.filter(name='big_graph_h')
def big_graph_h(src):
    return src.replace("graph_type=h", "").replace("graph_type=k", "").replace("graph_type=a", "").\
        replace("/chart/h", "/chart/big")


@register.filter(name='big_graph_k')
def big_graph_k(src):
    return src.replace("graph_type=h", "").replace("graph_type=k", "").replace("graph_type=a", "").\
        replace("/chart/k", "/chart/big")


@register.filter(name='big_graph_a')
def big_graph_a(src):
    return src.replace("graph_type=h", "").replace("graph_type=k", "").replace("graph_type=a", "").\
        replace("/chart/a", "/chart/big")


@register.filter(name='top_screen')
def top_screen(pid):
    try:
        top_screen = DashboardScreen.objects.get(id=pid).name
    except:
        top_screen = ''
    return top_screen


@register.filter(name='my_split')
def my_split(strl, arg):
    return strl.split(arg)


@register.filter(name='my_join')
def my_join(strl):
    return '\n'.join(strl)



@register.filter(name='list_0')
def list_0(char_str):
    return char_str[0]


@register.filter(name='list_1')
def list_1(char_str):
    return char_str[1]


@register.filter(name='get_env_name')
def get_env_name(code):
    try:
        return [i[1] for i in ENV if i[0] == int(code)][0]
    except:
        return ''


@register.filter(name='get_product_name')
def get_product_name(code):
    try:
        return [i[1] for i in LINE if i[0] == int(code)][0]
    except:
        return ''


@register.filter(name='get_status_name')
def get_status_name(code):
    try:
        print code
        return [i[1] for i in STATUS if i[0] == int(code)][0]
    except:
        return ''
