# encoding: utf-8

"""
@version: 
@author: liriqiang
@file: express_api.py
@time: 16-8-5 下午4:36
"""
import os
import sys
from subprocess import Popen, PIPE
import paramiko
from opsplatform.api import *
from models import *
from opsplatform.settings import RRKDINTERFACE_HOST, RRKDINTERFACE_PORT, RRKDINTERFACE_USERNAME, \
    RRKDINTERFACE_PASSWORD, RRKDINTERFACE_CLIENT_PATH, RRKDINTERFACE_COURIER_PATH, RRKDINTERFACE_MONI_HOST, \
    RRKDINTERFACE_MONI_PORT, RRKDINTERFACE_MONI_USERNAME, RRKDINTERFACE_MONI_PASSWORD, RRKDINTERFACE_MONI_CLIENT_PATH, \
    RRKDINTERFACE_MONI_COURIER_PATH, APK_HOST, APK_PORT, APK_USERNAME, APK_PASSWORD, APK_APK_PATH, APK_MONI_PATH

from ansible_api import *
from perm.ansible_api import ANSIBLE_DIR

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
        module_args = '/usr/bin/unison fr-web3;/usr/bin/unison web2;/usr/bin/unison web3'
        cmd = Command(module_name='shell', module_args=module_args, pattern=host)
        cmd.run()
        ret = cmd.result.get(host).get('dark', '')
        if ret:
            logger.info("发布进度: %s" % ret)
            raise ServerError(ret)
        result = cmd.state
        if not result.get('ok').get(host) and result.get('err'):
            logger.info("发布进度: %s" % result.get('err').get(host).get('stderr'))
            raise ServerError(result.get('err').get(host).get('stderr'))
        # s = paramiko.SSHClient()
        # s.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        # s.connect(hostname=host, port=port, username=username, password=password)
        # stdin, stdout, stderr = s.exec_command('/usr/bin/unison fr-web3;/usr/bin/unison web2;/usr/bin/unison web3')
        # logger.info("发布同步命令: %s" % stdout)
        # print stdin
        # s.close()


def update_file(file_path, param={}):
    """
    根据更新内容字典替换文件内容并提前做好备份
    :param file_path:
    :param param:
    :return:
    """
    mkdir(os.path.dirname(file_path) + '/backup')
    bash('cp ' + file_path + ' ' + os.path.dirname(file_path) + '/backup')

    for key, value in param.items():
        with open(file_path, 'r') as f:
            ls = f.readlines()
            i = 0
            for l in ls:
                if "'" + key + "'=>" in l:
                    if key == 'androidverremark' or \
                       key == 'androidsUpdateRemark' or \
                       key == 'iosUpdateRemark':
                        value = r"\r\n".join(value.split('\r\n'))
                    last = l.split('=>')[1]
                    lr = l.replace(last, "'" + value + "'" + ',\n')
                    ls[i] = lr
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


def project_deploy(publish_task, project, git_branch):
    """
    分别发布每一个机器
    发布完成后更新branch到最新
    :param project_id:
    :return:
    """
    try:
        publish_task_deploy = PublishTaskDeploy.objects.get(publish_task=publish_task)
        # 拉取仓库代码
        os.chdir(CODE_DIR)
        repository = ''.join(project.git_url.split('/')[-1].split('.')[:-1])
        if not os.path.exists(CODE_DIR + '/' + project.code):
            os.mkdir(CODE_DIR + '/' + project.code)
        repository_path = CODE_DIR + '/' + project.code + '/' + repository
        if not os.path.exists(repository_path):
            os.chdir(CODE_DIR + '/' + project.code)
            project.src = repository_path
            project.save()
            bash('git clone ' + project.git_url)
        os.chdir(repository_path)

        # 切换分支或者TAG

        logger.info("[拉取代码]: %s" % project.name)
        _, ttag, tag = git_branch.split('/')
        bash('git pull')
        if ttag == 'heads':
            bash('git checkout -b ' + tag + ' origin/' + tag)
            bash('git pull origin ' + tag)
        else:
            bash('git checkout ' + tag)
        publish_task_deploy.deploy_progress = int(publish_task_deploy.deploy_progress) + 1
        publish_task_deploy.deploy_info = publish_task_deploy.deploy_info + u'拉取代码...\n更新代码成功！\n'
        publish_task_deploy.save()

        if project.language_type == 'Java':
            # 本地构建JAVA 代码
            # 1.根据不同运行环境选择相应脚本执行
            logger.info("[编译代码]: %s" % project.name)
            path = os.environ['PATH']
            os.environ['PATH'] = path + ':/usr/local/maven/bin'
            if project.env == '2':
                print './build_simulate.sh'
                bash('chmod o+x build_simulate.sh')
                bash('./build_simulate.sh')
            elif project.env == '1':
                print './build_product.sh'
                bash('chmod o+x build_product.sh')
                bash('./build_product.sh')
            publish_task_deploy.deploy_progress = int(publish_task_deploy.deploy_progress) + 1
            publish_task_deploy.deploy_info = publish_task_deploy.deploy_info + u'构建JAVA代码...\n构建成功！\n'
            publish_task_deploy.save()

            # 2.停止tomcat
            logger.info("[停止tomcat]: %s" % project.name)
            module_args = "ps -ef |grep -w /usr/local/" + project.tomcat_num + " |grep -v grep |awk '{print $2}' |xargs kill -9"
            print module_args
            cmd = Command(module_name='shell', module_args=module_args, pattern=project.host)
            cmd.run()
            ret = cmd.result.get(project.host).get('dark', '')
            if ret:
                logger.info("[停止tomcat] 发布出错: %s" % ret)
                raise ServerError(ret)
            result = cmd.state
            print result
            if not result.get('ok').get(project.host) and result.get('err') and result.get('err').get(project.host).get('stderr'):
                logger.info("[停止tomcat] 发布出错: %s" % result.get('err').get(project.host).get('stderr'))
                raise ServerError(result.get('err').get(project.host).get('stderr'))
            publish_task_deploy.deploy_progress = int(publish_task_deploy.deploy_progress) + 1
            publish_task_deploy.deploy_info = publish_task_deploy.deploy_info + '停止tomcat...\n' + 'tomcat已停止\n'
            publish_task_deploy.save()

            # 3.备份原文件
            logger.info("[备份原文件]: %s" % project.name)
            module_args = 'chdir=' + project.dest + ' tar -zcvf ' + project.code + '.`date +%m%d%H`.tar.gz * ; mv ' + project.code + '.`date +%m%d%H`.tar.gz ' + project.backup_dir
            cmd = Command(module_name='shell', module_args=module_args, pattern=project.host)
            cmd.run()
            ret = cmd.result.get(project.host).get('dark', '')
            if ret:
                logger.info("[备份原文件] 发布出错: %s" % ret)
                raise ServerError(ret)
            result = cmd.state
            print result
            if not result.get('ok').get(project.host) and result.get('err') and result.get('err').get(project.host).get('stderr'):
                logger.info("[备份原文件] 发布出错: %s" % result.get('err').get(project.host).get('stderr'))
                raise ServerError(result.get('err').get(project.host).get('stderr'))
            publish_task_deploy.deploy_progress = int(publish_task_deploy.deploy_progress) + 1
            publish_task_deploy.deploy_info = publish_task_deploy.deploy_info + '备份原文件...\n' + '备份完成！\n'
            publish_task_deploy.save()

            # 4.删除旧文件
            logger.info("[删除旧文件]: %s" % project.name)
            module_args = 'rm -rf ' + project.dest + '/*'
            cmd = Command(module_name='shell', module_args=module_args, pattern=project.host)
            cmd.run()
            ret = cmd.result.get(project.host).get('dark', '')
            if ret:
                logger.info("[删除旧文件] 发布出错: %s" % ret)
                raise ServerError(ret)
            result = cmd.state
            print result
            if not result.get('ok').get(project.host) and result.get('err') and result.get('err').get(project.host).get('stderr'):
                logger.info("[删除旧文件] 发布出错: %s" % result.get('err').get(project.host).get('stderr'))
                raise ServerError(result.get('err').get(project.host).get('stderr'))
            publish_task_deploy.deploy_progress = int(publish_task_deploy.deploy_progress) + 1
            publish_task_deploy.deploy_info = publish_task_deploy.deploy_info + '删除旧文件...\n' + '删除旧文件完成!\n'
            publish_task_deploy.save()

            # 5.同步文件
            logger.info("[同步文件]: %s" % project.name)
            war_file = ''
            core_file = ''
            p = Popen('find * -name "*.war"', shell=True, stdout=PIPE, stderr=PIPE).stdout.readlines()
            if p:
                war_file = p[0].strip()
                print war_file
            if not war_file:
                p = Popen('find * -name "*.tar.gz"', shell=True, stdout=PIPE, stderr=PIPE).stdout.readlines()
                if p:
                    core_file = p[0].strip()

            src = war_file if war_file else core_file
            print 'WAR/GZ :   ' + src
            module_args = 'src=' + src + ' dest=' + project.dest + ' delete=' + project.is_full
            cmd = Command(module_name='synchronize', module_args=module_args, pattern=project.host)
            cmd.run()
            ret = cmd.result.get(project.host).get('dark', '')
            if ret:
                logger.info("[同步文件] 发布出错: %s" % ret)
                raise ServerError(ret)
            result = cmd.state
            if not result.get('ok').get(project.host) and result.get('err') and result.get('err').get(project.host).get('stderr'):
                logger.info("[同步文件] 发布出错: %s" % result.get('err').get(project.host).get('stderr'))
                raise ServerError(result.get('err').get(project.host).get('stderr'))
            publish_task_deploy.deploy_progress = int(publish_task_deploy.deploy_progress) + 1
            publish_task_deploy.deploy_info = publish_task_deploy.deploy_info + '同步文件...\n' + '同步文件完成!\n'
            publish_task_deploy.save()

            # 6.解压部署的压缩包
            logger.info("[解压部署的压缩包]: %s" % project.name)
            if core_file:
                file_name = os.path.basename(core_file)
                print file_name
                module_args = 'tar -zxvf ' + project.dest + '/' + file_name + ' -C ' + project.dest
                print module_args
                cmd = Command(module_name='shell', module_args=module_args, pattern=project.host)
                cmd.run()
                ret = cmd.result.get(project.host).get('dark', '')
                if ret:
                    logger.info("[解压压缩包] 发布出错: %s" % ret)
                    raise ServerError(ret)
                result = cmd.state
                if not result.get('ok').get(project.host) and result.get('err') and result.get('err').get(project.host).get('stderr'):
                    logger.info("[解压压缩包] 发布出错: %s" % result.get('err').get(project.host).get('stderr'))
                    raise ServerError(result.get('err').get(project.host).get('stderr'))

            # 7.启动tomcat
            logger.info("[启动tomcat]: %s" % project.name)
            module_args = 'chdir=/usr/local/' + project.tomcat_num + '/bin nohup ./startup.sh &'
            cmd = Command(module_name='shell', module_args=module_args, pattern=project.host)
            cmd.run()
            ret = cmd.result.get(project.host).get('dark', '')
            if ret:
                logger.info("[启动tomcat] 发布出错: %s" % ret)
                raise ServerError(ret)
            result = cmd.state
            if not result.get('ok').get(project.host) and result.get('err') and result.get('err').get(project.host).get('stderr'):
                logger.info("[启动tomcat] 发布出错: %s" % result.get('err').get(project.host).get('stderr'))
                raise ServerError(result.get('err').get(project.host).get('stderr'))
            publish_task_deploy.deploy_progress = int(publish_task_deploy.deploy_progress) + 1
            publish_task_deploy.deploy_info = publish_task_deploy.deploy_info + '启动tomcat...\n' + '启动tomcat完成!\n'
            publish_task_deploy.save()

            # 8.判断tomcat 是否启动成功
            logger.info("[判断tomcat 是否启动成功]: %s" % project.name)
            module_args = 'ps -ef |grep -w /usr/local/' + project.tomcat_num + "|grep -v grep |awk '{print $2}'"
            cmd = Command(module_name='shell', module_args=module_args, pattern=project.host)
            cmd.run()
            ret = cmd.result.get(project.host).get('dark', '')
            if ret:
                logger.info("[判断tomcat是否启动] 发布出错: %s" % ret)
                raise ServerError(ret)
            result = cmd.state
            if not result.get('ok').get(project.host) and result.get('err') and result.get('err').get(project.host).get('stderr'):
                logger.info("[判断tomcat是否启动] 发布出错: %s" % result.get('err').get(project.host).get('stderr'))
                raise ServerError(result.get('err').get(project.host).get('stderr'))
            print cmd.result
            if not cmd.result.get(project.host).get('stdout'):
                logger.info("[判断tomcat是否启动] 发布出错: %s" % '启动Tomcat失败')
                raise ServerError('启动Tomcat失败')
            publish_task_deploy.deploy_progress = int(publish_task_deploy.deploy_progress) + 1
            publish_task_deploy.deploy_info = publish_task_deploy.deploy_info + '判断tomcat是否启动成功...\n' + 'tomcat已启动成功!\n发布完成，请返回!'
            publish_task_deploy.save()
            print 'over:======\n' + publish_task_deploy.deploy_info
        elif project.language_type == 'PHP':
            exclude_from = ANSIBLE_DIR + "/exclude_from"
            with open(exclude_from, 'w') as f:
                    f.write(project.ignore_setup)
            src = os.getcwd() + '/'
            # 1.备份原文件
            logger.info("[备份原文件]: %s" % project.name)
            module_args = 'chdir=' + project.dest + ' tar -zcvf ' + project.code + '.`date +%m%d%H`.tar.gz * ; mv ' + project.code + '.`date +%m%d%H`.tar.gz ' + project.backup_dir
            cmd = Command(module_name='shell', module_args=module_args, pattern=project.host)
            cmd.run()
            ret = cmd.result.get(project.host).get('dark', '')
            if ret:
                logger.info("[备份原文件] 发布出错: %s" % ret)
                raise ServerError(ret)
            result = cmd.state
            print result
            if not result.get('ok').get(project.host) and result.get('err') and result.get('err').get(project.host).get('stderr'):
                logger.info("[备份原文件] 发布出错: %s" % result.get('err').get(project.host).get('stderr'))
                raise ServerError(result.get('err').get(project.host).get('stderr'))
            publish_task_deploy.deploy_progress = int(publish_task_deploy.deploy_progress) + 1
            publish_task_deploy.deploy_info = publish_task_deploy.deploy_info + '备份原文件...\n' + '备份原文件成功!\n'
            publish_task_deploy.save()

            # 2.同步文件
            logger.info("[同步文件]: %s" % project.name)
            module_args = 'src=' + src + ' dest=' + project.dest + ' delete=' + project.is_full + ' rsync_opts=--exclude-from=' + exclude_from
            cmd = Command(module_name='synchronize', module_args=module_args, pattern=project.host)
            cmd.run()
            ret = cmd.result.get(project.host).get('dark', '')
            if ret:
                logger.info("[同步文件] 发布出错: %s" % ret)
                raise ServerError(ret)
            result = cmd.state
            if not result.get('ok').get(project.host) and result.get('err') and result.get('err').get(project.host).get('stderr'):
                logger.info("[同步文件] 发布出错: %s" % result.get('err').get(project.host).get('stderr'))
                raise ServerError(result.get('err').get(project.host).get('stderr'))
            publish_task_deploy.deploy_progress = int(publish_task_deploy.deploy_progress) + 1
            publish_task_deploy.deploy_info = publish_task_deploy.deploy_info + '同步文件...\n' + '同步文件成功!\n'
            publish_task_deploy.save()

            # 3.修改文件权限
            logger.info("[修改文件权限]: %s" % project.name)
            module_args = 'chown -R www:www ' + project.dest
            cmd = Command(module_name='shell', module_args=module_args, pattern=project.host)
            cmd.run()
            print cmd.result
            print cmd.state
            ret = cmd.result.get(project.host).get('dark', '')
            print ret, ret == ''
            if ret:
                logger.info("[修改文件权限] 发布出错: %s" % ret)
                raise ServerError(ret)
            result = cmd.state
            if not result.get('ok').get(project.host) and result.get('err') and result.get('err').get(project.host).get('stderr'):
                print result.get('err').get(project.host).get('stderr')
                logger.info("[修改文件权限] 发布出错: %s" % result.get('err').get(project.host).get('stderr'))
                raise ServerError(result.get('err').get(project.host).get('stderr'))
            publish_task_deploy.deploy_progress = int(publish_task_deploy.deploy_progress) + 1
            publish_task_deploy.deploy_info = publish_task_deploy.deploy_info + '修改文件权限...\n' + '修改文件权限成功!\n发布完成，请返回!'
            publish_task_deploy.save()

        else:
            logger.info("不支持自动发布！")
            raise ServerError('不支持自动发布！')
    except Exception as e:
        print '异常输出： ' + str(e)
        logger.info("发布出错: %s" % '发布过程出错')
        publish_task_deploy.deploy_info = publish_task_deploy.deploy_info + '\n===============\n发布出错:' + str(e)
        publish_task_deploy.deploy_total = 0
        publish_task_deploy.save()
        return False
    return True


def publish_task_deploy_run(task_id, deploy_type):
    publish_task = get_object(PublishTask, id=task_id)

    if deploy_type == u'全网更新':
        projects = Project.objects.filter(name=publish_task.project, env=publish_task.env)
    else:
        projects = Project.objects.filter(name=publish_task.project, env=publish_task.env, idc=deploy_type)
    # 计算发布需要多少步
    total = len(projects) * (4 if projects[0].language_type == 'PHP' else 8)
    obj, created = PublishTaskDeploy.objects.get_or_create(publish_task=publish_task)
    obj.deploy_total = total
    obj.deploy_progress = 0
    obj.deploy_info = ''
    obj.save()
    for project in projects:
        try:
            if not project_deploy(publish_task, project, publish_task.code_tag):
                return False
        except Exception as e:
            print e
            logger.info("发布进度: %s" % e)
            return False

    return True


def publish_task_rollback_run(publish_task):
    # 自动化发布过的代码从备份里恢复最新的备份
    if publish_task.idc == u'全网更新':
        projects = Project.objects.filter(name=publish_task.project, env=publish_task.env)
    else:
        projects = Project.objects.filter(name=publish_task.project, env=publish_task.env, idc=publish_task.idc)
    print projects

    # 回滚备份文件
    try:
        for project in projects:
            module_args = 'chdir=' + project.backup_dir + ' tar -zxvf  `ls -t|grep ' + project.code + '|head -n1` -C ' + project.dest
            print module_args
            cmd = Command(module_name='shell', module_args=module_args, pattern=project.host)
            cmd.run()
            ret = cmd.result.get(project.host).get('dark', '')
            if ret:
                logger.info("发布进度: %s" % ret)
                return False
            result = cmd.state
            print result
            if not result.get('ok').get(project.host):
                logger.info("发布进度: %s" % result.get('err').get(project.host).get('stderr'))
                return False
    except Exception as e:
        print e
        logger.info("发布进度: %s" % e)
        return False
    return True


def plist_setup(app_type, version, env):
    try:
        ipa_name = app_type + '_' + version + '_' + env + '.ipa'
        print ipa_name
        # 修改 plist 文件
        plist_path = (CLIENT_IPA_PATH if app_type == 'RrkdClient' else COURIER_IPA_PATH) + '/' + app_type + '_' + env + '.plist'
        with open(plist_path, 'r') as f:
            ls = f.readlines()
            i = 0
            for l in ls:
                if '<key>url</key>' in l:
                    ls[i+1] = '<string>' + 'https://oerfptemy.qnssl.com/' + ipa_name + '</string>\n'
                    print ls
                elif '<key>bundle-version</key>' in l:
                    ls[i+1] = '<string>' + version + '</string>\n'
                    print ls
                i = i + 1

        with open(plist_path, 'w') as fw:
            fw.write(''.join(ls))

        # 同步到远程服务器
        host = IPA_REMOTE_HOST
        plist_remote_path = (CLIENT_IPA_REMOTE_PATH if app_type == 'RrkdClient' else COURIER_IPA_REMOTE_PATH) + '/' + app_type + '_' + env + '.plist'
        module_args = 'src=' + plist_path + ' dest=' + plist_remote_path
        cmd = Command(module_name='synchronize', module_args=module_args, pattern=host)
        cmd.run()
        ret = cmd.result.get(host).get('dark', '')
        if ret:
            logger.info("[同步文件] 配置IPA出错: %s" % ret)
            raise ServerError(ret)
        result = cmd.state
        if not result.get('ok').get(host) and result.get('err') and result.get('err').get(host).get('stderr'):
            logger.info("[同步文件] 配置IPA出错: %s" % result.get('err').get(host).get('stderr'))
            raise ServerError(result.get('err').get(host).get('stderr'))
    except Exception as e:
        print e
        return False
    return True


def handle_uploaded_file(path, f):
    file_name = ""

    try:
        path = path + time.strftime('/%Y/%m/%d/%H/%M/%S/')
        if not os.path.exists(path):
            os.makedirs(path)
            file_name = path + f.name
            destination = open(file_name, 'wb+')
            for chunk in f.chunks():
                destination.write(chunk)
            destination.close()
    except Exception, e:
        print e

    return file_name