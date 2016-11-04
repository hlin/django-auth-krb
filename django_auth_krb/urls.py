from django.conf.urls import url
from django.contrib.auth.views import login
from django.contrib.auth.views import logout

urlpatterns = [
    url(r'^login/$', login,
        kwargs={'redirect_authenticated_user': True}, name='login'),
    url(r'^logout/$', logout, name='logout'),
]
