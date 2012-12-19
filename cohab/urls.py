from django.conf.urls import patterns, include, url

from django.contrib import admin
admin.autodiscover()

from lib.views import LoginView, LogoutView

from tastypie.api import Api
from todo.resources import TaskResource, TaskAreaResource, TaskActionResource
from lib.resources import UserResource

v1_api = Api(api_name='v1')
v1_api.register(TaskResource())
v1_api.register(TaskActionResource())
v1_api.register(TaskAreaResource())
v1_api.register(UserResource())

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'cohab.views.home', name='home'),
    url(r'^cohab/', include('todo.urls', namespace='todo')),

    url(r'^login$', LoginView.as_view(), name="login"),
    url(r'^logout$', LogoutView.as_view(), name="logout"),

    url(r'^admin/doc/', include('django.contrib.admindocs.urls')),
    url(r'^admin/', include(admin.site.urls)),

    url(r'^rest/', include(v1_api.urls))
)
