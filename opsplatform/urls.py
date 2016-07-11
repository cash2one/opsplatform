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
from django.conf.urls import url, include
from opsplatform import views
from account.api.uic import *


urlpatterns = [
    # Examples:
    url(r'^$', views.index, name='index'),
    url(r'^skin_config/$', views.skin_config, name='skin_config'),
    url(r'^login', views.Login, name='login'),
    url(r'^logout/$', views.Logout, name='logout'),
    url(r'^exec_cmd/$', views.exec_cmd, name='exec_cmd'),
    url(r'^terminal/$', views.web_terminal, name='terminal'),
    url(r'^file/upload/$', views.upload, name='file_upload'),
    url(r'^file/download/$', views.download, name='file_download'),
    url(r'^account/', include('account.urls')),
    url(r'^asset/', include('asset.urls')),
    url(r'^perm/', include('perm.urls')),
    url(r'^jlog/', include('jlog.urls')),
    url(r'^monitor/', include('monitor.urls')),

    url(r'^note_list/$', views.note_list, name='note_list'),

    # api url
    url(r'^sso/sig$', sso_sig, name='sso_sig'),
    url(r'^sso/user/(?P<sig>.+)$', sso_user, name='sso_user'),
    url(r'^auth/login$', auth_login, name='auth_login'),
    url(r'^team/query$', team_query, name='team_query'),
    url(r'^team/users$', team_users, name='team_users'),
    url(r'^team/all$', team_all, name='team_all'),
    url(r'^user/in$', user_in, name='user_in'),
    url(r'^about/(?P<user>.+)$', about_user, name='about_user')
]
