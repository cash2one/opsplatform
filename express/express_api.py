# encoding: utf-8

"""
@version: 
@author: liriqiang
@file: express_api.py
@time: 16-8-5 下午4:36
"""
import os
import sys
import paramiko
from opsplatform.api import *
from models import *
from opsplatform.settings import RRKDINTERFACE_HOST, RRKDINTERFACE_PORT, RRKDINTERFACE_USERNAME, \
    RRKDINTERFACE_PASSWORD, RRKDINTERFACE_CLIENT_PATH, RRKDINTERFACE_COURIER_PATH, RRKDINTERFACE_MONI_HOST, \
    RRKDINTERFACE_MONI_PORT, RRKDINTERFACE_MONI_USERNAME, RRKDINTERFACE_MONI_PASSWORD, RRKDINTERFACE_MONI_CLIENT_PATH, \
    RRKDINTERFACE_MONI_COURIER_PATH, APK_HOST, APK_PORT, APK_USERNAME, APK_PASSWORD, APK_APK_PATH, APK_MONI_PATH

from perm.ansible_api import *

default_encoding = 'utf-8'
if sys.getdefaultencoding() != default_encoding:
    reload(sys)
    sys.setdefaultencoding(default_encoding)


def download_file(env, localpath, remotepath):
    """
    下载配置文件
    :return:
    """
    if env == '1':
        host = RRKDINTERFACE_HOST
        port = int(RRKDINTERFACE_PORT)
        username = RRKDINTERFACE_USERNAME
        password = RRKDINTERFACE_PASSWORD
    elif env == '2':
        host = RRKDINTERFACE_MONI_HOST
        port = int(RRKDINTERFACE_MONI_PORT)
        username = RRKDINTERFACE_MONI_USERNAME
        password = RRKDINTERFACE_MONI_PASSWORD
    t = paramiko.Transport((host, port))
    t.connect(username=username, password=password)
    sftp = paramiko.SFTPClient.from_transport(t)
    sftp.get(remotepath, localpath)
    t.close()


def upload_apk(localpath, remotepath):

    t = paramiko.Transport((APK_HOST, int(APK_PORT)))
    t.connect(username=APK_USERNAME, password=APK_PASSWORD)
    sftp = paramiko.SFTPClient.from_transport(t)
    sftp.put(localpath, remotepath)
    t.close()


def upload_config(env, localpath, remotepath):
    if env == '1':
        host = RRKDINTERFACE_HOST
        port = int(RRKDINTERFACE_PORT)
        username = RRKDINTERFACE_USERNAME
        password = RRKDINTERFACE_PASSWORD
    elif env == '2':
        host = RRKDINTERFACE_MONI_HOST
        port = int(RRKDINTERFACE_MONI_PORT)
        username = RRKDINTERFACE_MONI_USERNAME
        password = RRKDINTERFACE_MONI_PASSWORD
    t = paramiko.Transport((host, port))
    t.connect(username=username, password=password)
    sftp = paramiko.SFTPClient.from_transport(t)
    sftp.put(localpath, remotepath)
    t.close()
    if env == '1':
        s = paramiko.SSHClient()
        s.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        s.connect(hostname=host, port=port, username=username, password=password)
        stdin, stdout, stderr = s.exec_command('/usr/bin/unison fr-web3;/usr/bin/unison web2;/usr/bin/unison web3')
        logger.info("发布同步命令: %s" % stdout)
        print stdin
        s.close()


def update_file(file_path, param={}):
    """
    根据更新内容字典替换文件内容并提前做好备份
    :param file_path:
    :param param:
    :return:
    """
    mkdir(os.path.dirname(file_path) + '/backup')
    bash('cp ' + file_path + ' ' + os.path.dirname(file_path) + '/backup')

    print param
    for key, value in param.items():
        with open(file_path, 'r') as f:
            ls = f.readlines()
            i = 0
            for l in ls:
                if "'" + key + "'=>" in l:
                    print ls
                    last = l.split('=>')[1].split(',')[0]
                    lr = l.replace(last, "'" + value + "'")
                    ls[i] = lr
                    print lr
                    print ls
                    break
                i = i + 1

        with open(file_path, 'w') as fw:
            fw.write(''.join(ls))


def app_publish_task_express(task_id):
    """
    进行发布任务
    0. 上传APK文件
    1. 拉取线上配置文件
    2. 更新配置文件
    3. 上传配置文件
    :param task_id:
    :return:
    """
    app_publish_task = get_object(AppPublishTask, id=task_id)
    if app_publish_task.style == '1' and app_publish_task.platform == '1':
        # 上传 APK
        apk_name = os.path.basename(app_publish_task.client_apk_path)
        if app_publish_task.env == '1':
            upload_apk("../publish_center/" + app_publish_task.client_apk_path, APK_APK_PATH + apk_name)
        elif app_publish_task.env == '2':
            upload_apk("../publish_center/" + app_publish_task.client_apk_path, APK_MONI_PATH + apk_name)

        localpath = 'data/' + app_publish_task.seq_no
        mkdir(localpath)

        # 修改system.php配置文件
        if app_publish_task.env == '1':
            download_file(app_publish_task.env, localpath + "/system.php", RRKDINTERFACE_CLIENT_PATH + 'system.php')
        elif app_publish_task.env == '2':
            download_file(app_publish_task.env, localpath + "/system.php", RRKDINTERFACE_MONI_CLIENT_PATH + 'system.php')

        data = {'AndroidPublishVersion': app_publish_task.client_sys_AndroidPublishVersion,
                'isforcedupdate': app_publish_task.client_sys_Androidisforcedupdate}
        update_file(localpath + "/system.php", data)
        if app_publish_task.env == '1':
            upload_config(app_publish_task.env, localpath + "/system.php", RRKDINTERFACE_CLIENT_PATH + 'system.php')
        elif app_publish_task.env == '2':
            upload_config(app_publish_task.env, localpath + "/system.php", RRKDINTERFACE_MONI_CLIENT_PATH + 'system.php')
        # 修改config.php配置文件
        if app_publish_task.env == '1':
            download_file(app_publish_task.env, localpath + "/config.php", RRKDINTERFACE_CLIENT_PATH + 'config.php')
        elif app_publish_task.env == '2':
            download_file(app_publish_task.env, localpath + "/config.php", RRKDINTERFACE_MONI_CLIENT_PATH + 'config.php')
        data = {'androidversion': app_publish_task.client_config_androidversion,
                'androidsjversion': app_publish_task.client_config_androidsjversion,
                'downloadandroidpath': app_publish_task.client_config_downloadandroidpath,
                'androidverremark': app_publish_task.client_config_androidverremark,
                'androidsUpdateRemark': app_publish_task.client_config_androidsUpdateRemark}
        update_file(localpath + "/config.php", data)
        if app_publish_task.env == '1':
            upload_config(app_publish_task.env, localpath + "/config.php", RRKDINTERFACE_CLIENT_PATH + 'config.php')
        elif app_publish_task.env == '2':
            upload_config(app_publish_task.env, localpath + "/config.php", RRKDINTERFACE_MONI_CLIENT_PATH + 'config.php')

    elif app_publish_task.style == '1' and app_publish_task.platform == '2':
        localpath = 'data/' + app_publish_task.seq_no
        mkdir(localpath)

        # 修改system.php配置文件
        if app_publish_task.env == '1':
            download_file(app_publish_task.env, localpath + "/system.php", RRKDINTERFACE_CLIENT_PATH + "system.php")
        elif app_publish_task.env == '2':
            download_file(app_publish_task.env, localpath + "/system.php", RRKDINTERFACE_MONI_CLIENT_PATH + "system.php")

        data = {'IOSPublishVersion': app_publish_task.client_sys_IOSPublishVersion,
                'isforcedupdate': app_publish_task.client_sys_IOSisforcedupdate}
        update_file(localpath + "/system.php", data)
        if app_publish_task.env == '1':
            upload_config(app_publish_task.env, localpath + "/system.php", RRKDINTERFACE_CLIENT_PATH + "system.php")
        elif app_publish_task.env == '2':
            upload_config(app_publish_task.env, localpath + "/system.php", RRKDINTERFACE_MONI_CLIENT_PATH + "system.php")
        # 修改config.php配置文件
        if app_publish_task.env == '1':
            download_file(app_publish_task.env, localpath + "/config.php", RRKDINTERFACE_CLIENT_PATH + 'config.php')
        elif app_publish_task.env == '2':
            download_file(app_publish_task.env, localpath + "/config.php", RRKDINTERFACE_MONI_CLIENT_PATH + 'config.php')
        data = {'iossjversion': app_publish_task.client_config_iossjversion,
                'iosUpdateRemark': app_publish_task.client_config_iosUpdateRemark,
                'iosverremark': app_publish_task.client_config_iosverremark
                }
        update_file(localpath + "/config.php", data)
        if app_publish_task.env == '1':
            upload_config(app_publish_task.env, localpath + "/config.php", RRKDINTERFACE_CLIENT_PATH + 'config.php')
        elif app_publish_task.env == '2':
            upload_config(app_publish_task.env, localpath + "/config.php", RRKDINTERFACE_MONI_CLIENT_PATH + 'config.php')

    elif app_publish_task.style == '2' and app_publish_task.platform == '1':
        # 上传 APK
        apk_name = os.path.basename(app_publish_task.courier_apk_path)
        if app_publish_task.env == '1':
            upload_apk("../publish_center/" + app_publish_task.courier_apk_path, APK_APK_PATH + apk_name)
        elif app_publish_task.env == '2':
            upload_apk("../publish_center/" + app_publish_task.courier_apk_path, APK_MONI_PATH + apk_name)

        localpath = 'data/' + app_publish_task.seq_no
        mkdir(localpath)

        # 修改system.php配置文件
        if app_publish_task.env == '1':
            download_file(app_publish_task.env, localpath + "/system.php", RRKDINTERFACE_COURIER_PATH + 'system.php')
        elif app_publish_task.env == '2':
            download_file(app_publish_task.env, localpath + "/system.php", RRKDINTERFACE_MONI_COURIER_PATH + 'system.php')

        data = {'AndroidPublishVersion': app_publish_task.courier_sys_AndroidPublishVersion,
                'isforcedupdate': app_publish_task.courier_sys_Androidisforcedupdate}
        update_file(localpath + "/system.php", data)
        if app_publish_task.env == '1':
            upload_config(app_publish_task.env, localpath + "/system.php", RRKDINTERFACE_COURIER_PATH + 'system.php')
        elif app_publish_task.env == '2':
            upload_config(app_publish_task.env, localpath + "/system.php", RRKDINTERFACE_MONI_COURIER_PATH + 'system.php')
        # 修改config.php配置文件
        if app_publish_task.env == '1':
            download_file(app_publish_task.env, localpath + "/config.php", RRKDINTERFACE_COURIER_PATH + 'config.php')
        elif app_publish_task.env == '2':
            download_file(app_publish_task.env, localpath + "/config.php", RRKDINTERFACE_MONI_COURIER_PATH + 'config.php')
        data = {'androidversion': app_publish_task.courier_config_androidversion,
                'androidsjversion': app_publish_task.courier_config_androidsjversion,
                'downloadandroidpath': app_publish_task.courier_config_downloadandroidpath,
                'androidverremark': app_publish_task.courier_config_androidverremark,
                'androidsUpdateRemark': app_publish_task.courier_config_androidsUpdateRemark}
        update_file(localpath + "/config.php", data)
        if app_publish_task.env == '1':
            upload_config(app_publish_task.env, localpath + "/config.php", RRKDINTERFACE_COURIER_PATH + 'config.php')
        elif app_publish_task.env == '2':
            upload_config(app_publish_task.env, localpath + "/config.php", RRKDINTERFACE_MONI_COURIER_PATH + 'config.php')

    elif app_publish_task.style == '2' and app_publish_task.platform == '2':
        localpath = 'data/' + app_publish_task.seq_no
        mkdir(localpath)

        # 修改system.php配置文件
        if app_publish_task.env == '1':
            download_file(app_publish_task.env, localpath + "/system.php", RRKDINTERFACE_COURIER_PATH + 'system.php')
        elif app_publish_task.env == '2':
            download_file(app_publish_task.env, localpath + "/system.php", RRKDINTERFACE_MONI_COURIER_PATH + 'system.php')

        data = {'IOSPublishVersion': app_publish_task.courier_sys_IOSPublishVersion,
                'isforcedupdate': app_publish_task.courier_sys_IOSisforcedupdate}
        update_file(localpath + "/system.php", data)
        if app_publish_task.env == '1':
            upload_config(app_publish_task.env, localpath + "/system.php", RRKDINTERFACE_COURIER_PATH + 'system.php')
        elif app_publish_task.env == '2':
            upload_config(app_publish_task.env, localpath + "/system.php", RRKDINTERFACE_MONI_COURIER_PATH + 'system.php')
        # 修改config.php配置文件
        if app_publish_task.env == '1':
            download_file(app_publish_task.env, localpath + "/config.php", RRKDINTERFACE_COURIER_PATH + 'config.php')
        elif app_publish_task.env == '2':
            download_file(app_publish_task.env, localpath + "/config.php", RRKDINTERFACE_MONI_COURIER_PATH + 'config.php')
        data = {'iossjversion': app_publish_task.courier_config_iossjversion,
                'iosUpdateRemark': app_publish_task.courier_config_iosUpdateRemark,
                'iosverremark': app_publish_task.courier_config_iosverremark
                }
        update_file(localpath + "/config.php", data)
        if app_publish_task.env == '1':
            upload_config(app_publish_task.env, localpath + "/config.php", RRKDINTERFACE_COURIER_PATH + 'config.php')
        elif app_publish_task.env == '2':
            upload_config(app_publish_task.env, localpath + "/config.php", RRKDINTERFACE_MONI_COURIER_PATH + 'config.php')


def app_publish_task_rollback_config(task_id):
    """
    回滚配置文件
    :param task_id:
    :return:
    """
    app_publish_task = get_object(AppPublishTask, id=task_id)
    localpath = 'data/' + app_publish_task.seq_no
    if app_publish_task.style == '1':
        if app_publish_task.env == '1':
            upload_config(app_publish_task.env, localpath + "/backup/system.php", RRKDINTERFACE_CLIENT_PATH + 'system.php')
            upload_config(app_publish_task.env, localpath + "/backup/config.php", RRKDINTERFACE_CLIENT_PATH + 'config.php')
        elif app_publish_task.env == '2':
            upload_config(app_publish_task.env, localpath + "/backup/system.php", RRKDINTERFACE_MONI_CLIENT_PATH + 'system.php')
            upload_config(app_publish_task.env, localpath + "/backup/config.php", RRKDINTERFACE_MONI_CLIENT_PATH + 'config.php')
    elif app_publish_task.style == '2':
        if app_publish_task.env == '1':
            upload_config(app_publish_task.env, localpath + "/backup/system.php", RRKDINTERFACE_COURIER_PATH + 'system.php')
            upload_config(app_publish_task.env, localpath + "/backup/config.php", RRKDINTERFACE_COURIER_PATH + 'config.php')
        elif app_publish_task.env == '2':
            upload_config(app_publish_task.env, localpath + "/backup/system.php", RRKDINTERFACE_MONI_COURIER_PATH + 'system.php')
            upload_config(app_publish_task.env, localpath + "/backup/config.php", RRKDINTERFACE_MONI_COURIER_PATH + 'config.php')


def project_deploy(project, git_branch):
    """
    分别发布每一个机器
    发布完成后更新branch到最新
    :param project_id:
    :return:
    """
    try:
        # 拉取仓库代码
        logger.info("构建代码: %s" % "切换到代码目录")
        os.chdir(CODE_DIR)
        print os.getcwd()
        repository = ''.join(project.git_url.split('/')[-1].split('.')[:-1])
        print repository
        if not os.path.exists(CODE_DIR + '/' + project.code):
            os.mkdir(CODE_DIR + '/' + project.code)
        repository_path = CODE_DIR + '/' + project.code + '/' + repository
        if not os.path.exists(repository_path):
            logger.info("构建代码: %s" % "首次发布克隆代码")
            os.chdir(CODE_DIR + '/' + project.code)
            bash('git clone ' + project.git_url)
        logger.info("构建代码: %s" % "进入代码仓库")
        os.chdir(repository_path)
        print os.getcwd()
        logger.info("构建代码: %s %s" % ("执行checkout分支 ", git_branch))
        print 'git checkout ' + git_branch
        bash('git checkout ' + git_branch)
        print 'git pull origin ' + git_branch
        bash('git pull origin ' + git_branch)
        # JAVA语言MVN构建代码
        if project.language_type == 'Java':
            logger.info("构建代码: %s", "Java mvn 构建中....")
            print 'mvn clean install -Dmaven.test.skip=true -P%s' % [i[1] for i in MVN_ENV if i[0] == project.env][0]
            # bash('mvn clean install -Dmaven.test.skip=true -P%s' % [i[1] for i in MVN_ENV if i[0] == project.env][0])
            #调用 ansible 完成服务器代码部署和服务重启
            # deploy_cmd = """ansible-playbook -e""" + \
            #              """ "Host=%s IsFull=%s Tomcat_Num=%s Src=%s Dest=%s Product_Name=%s Backup_Dir=%s " """ % \
            #              (project.host, project.is_full, project.tomcat_num, os.getcwd(), project.dest, project.code, project.backup_dir) +\
            #              ANSIBLE_DIR + """/deploy_java.yaml"""
            # bash(deploy_cmd)
        elif project.language_type == 'PHP':
            exclude_from = ANSIBLE_DIR + "/exclude_from"
            with open(exclude_from, 'w') as f:
                f.write(project.ignore_setup)
            src = os.getcwd() + '/'
            deploy_cmd = """ansible-playbook -e """ + \
                         """ "Host=%s IsFull=%s Src=%s Dest=%s Product_Name=%s Backup_Dir=%s Exclude_from=%s" """ % \
                         (project.host, project.is_full, src, project.dest, project.code, project.backup_dir, exclude_from) +\
                         ANSIBLE_DIR + """/deploy_php.yaml"""
            print deploy_cmd
            bash(deploy_cmd)
    except Exception as e:
        print e
        logger.debug("发布进度: %s" % '发布过程出错')
        raise ServerError('发布过程出错')


def publish_task_deploy_run(task_id, deploy_type):
    publish_task = get_object(PublishTask, id=task_id)

    if deploy_type == u'全网更新':
        projects = Project.objects.filter(name=publish_task.project, env=publish_task.env)
    else:
        projects = Project.objects.filter(name=publish_task.project, env=publish_task.env, idc=deploy_type)
    print projects
    print task_id
    for project in projects:
        try:
            project_deploy(project, publish_task.code_tag)
        except Exception as e:
            print e
            logger.debug("发布进度: %s" % e)
            return False

    return False

