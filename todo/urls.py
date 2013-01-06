from django.conf.urls import patterns, url  # , include
from django.views.generic import TemplateView
from todo.views import TodoList, AreaView, AreaList, ActionView, ActionList
from todo.views import UserView

urlpatterns = patterns('',
    url(r'^$', TemplateView.as_view(template_name="home.html"), name="home"),
    url(r'^todo$', TodoList.as_view(), name="list_tasks"),
    url(r'^user/(?P<slug>\w+[-\w\d]+)/$', UserView.as_view(), name="show_user"),
    url(r'^areas/', AreaList.as_view(), name="list_areas"),
    url(r'^area/(?P<slug>\w+[-\w\d]+)/$', AreaView.as_view(), name="show_area"),
    url(r'^lists/', ActionList.as_view(), name="list_actions"),
    url(r'^list/(?P<slug>\w+[-\w\d]+)/$', ActionView.as_view(), name="show_action"),
)
