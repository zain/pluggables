from django.conf.urls.defaults import *
from appdir.models import App

urlpatterns = patterns('',
    url('^$', 'django.views.generic.list_detail.object_list', dict(
        queryset=App.objects.all(),
        paginate_by=25,
        template_name='appdir/app_list.html',
        template_object_name='app',
    )),
    url('^(?P<slug>[\w-]+)/$', 'django.views.generic.list_detail.object_detail', dict(
        queryset=App.objects.all(),
        template_name='appdir/app_detail.html',
        template_object_name='app',
    )),
)