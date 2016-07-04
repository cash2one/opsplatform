"""opsplatform URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.9/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url
from account import views


urlpatterns = [
    url(r'^group/list/$', views.group_list, name='user_group_list'),
    url(r'^group/add/$', views.group_add, name='user_group_add'),
    url(r'^group/edit/$', views.group_edit, name='user_group_edit'),
    url(r'^group/detail/$', views.group_detail, name='user_group_detail'),
    url(r'^group/del/$', views.group_del, name='user_group_del'),

    url(r'^user/list/$', views.user_list, name='user_list'),
    url(r'^user/add/$', views.user_add, name='user_add'),
    url(r'^user/edit/$', views.user_edit, name='user_edit'),
    url(r'^user/detail/$', views.user_detail, name='user_detail'),
    url(r'^user/del/$', views.user_del, name='user_del'),

    url(r'^user/profile/$', views.profile, name='user_profile'),
    url(r'^user/update/$', views.change_info, name='user_update'),

    url(r'^password/reset/$', views.reset_password, name='password_reset'),
    url(r'^password/forget/$', views.forget_password, name='password_forget'),
    url(r'^mail/retry/$', views.send_mail_retry, name='mail_retry'),
    url(r'^key/gen/$', views.regen_ssh_key, name='key_gen'),
    url(r'^key/down/$', views.down_key, name='key_down'),

]
