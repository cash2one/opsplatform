# encoding: utf-8

"""
@version: 
@author: liriqiang
@file: setup.py.py
@time: 16-6-13 下午2:11
"""
import os
import sys
import time
import shlex
import django
from django.core.management import execute_from_command_line
from opsplatform.api import get_object
from account.models import User
from account.user_api import db_add_user

ops_dir = os.path.dirname(os.path.abspath(os.path.dirname(__file__)))
sys.path.append(ops_dir)

os.environ['DJANGO_SETTINGS_MODULE'] = 'opsplatform.settings'
if django.get_version() != '1.6':
    setup = django.setup()


def color_print(msg, color='red', exits=False):
    """
    Print colorful string.
    颜色打印字符或者退出
    """
    color_msg = {'blue': '\033[1;36m%s\033[0m',
                 'green': '\033[1;32m%s\033[0m',
                 'yellow': '\033[1;33m%s\033[0m',
                 'red': '\033[1;31m%s\033[0m',
                 'title': '\033[30;42m%s\033[0m',
                 'info': '\033[32m%s\033[0m'}
    msg = color_msg.get(color, 'red') % msg
    print msg
    if exits:
        time.sleep(2)
        sys.exit()
    return msg


class Setup(object):

    def __init__(self):
        self.admin_user = 'admin'
        self.admin_pass = 'cwkj123456'

    @staticmethod
    def _chmod_file():
        os.chdir(ops_dir)
        os.chmod('init.sh', 0755)
        os.chmod('connect.py', 0755)
        os.chmod('manage.py', 0755)
        os.chmod('run_server.py', 0755)
        os.chmod('service.sh', 0755)
        os.chmod('logs', 0777)
        os.chmod('keys', 0777)

    def _input_admin(self):
        while True:
            print
            admin_user = raw_input('请输入管理员用户名 [%s]: ' % self.admin_user).strip()
            admin_pass = raw_input('请输入管理员密码: [%s]: ' % self.admin_pass).strip()
            admin_pass_again = raw_input('请再次输入管理员密码: [%s]: ' % self.admin_pass).strip()

            if admin_user:
                self.admin_user = admin_user

            if not admin_pass_again:
                admin_pass_again = self.admin_pass

            if admin_pass:
                self.admin_pass = admin_pass

            if self.admin_pass != admin_pass_again:
                color_print('两次密码不相同请重新输入')
            else:
                break
            print

    @staticmethod
    def _sync_db():
        os.chdir(ops_dir)
        execute_from_command_line(['manage.py', 'migrate'])

    def _create_admin(self):
        user = get_object(User, username=self.admin_user)
        if user:
            user.delete()
        db_add_user(username=self.admin_user, password=self.admin_pass, role='SU', name='admin', groups='',
                    admin_groups='', email='admin@rrkd.cn', uuid='MayBeYouAreTheFirstUser', is_active=True)
        cmd = 'id %s 2> /dev/null 1> /dev/null || useradd %s' % (self.admin_user, self.admin_user)
        shlex.os.system(cmd)

    @staticmethod
    def _run_service():
        cmd = 'bash %s start' % os.path.join(ops_dir, 'service.sh')
        shlex.os.system(cmd)
        print
        color_print('安装成功，请访问web, 祝你使用愉快。', 'green')

    def start(self):
        print "开始安装Opsplatform ..."
        self._sync_db()
        self._input_admin()
        self._create_admin()
        self._chmod_file()
        self._run_service()

if __name__ == '__main__':
    setup = Setup()
    setup.start()
