from django.conf.urls import patterns, url  # , include
from django.views.generic import TemplateView
from todo.views import AreaView, AreaList, ActionView, ActionList
from todo.views import AddToUser, AddToList, AddToArea, AddTask
from todo.views import UserView, TodoList
from todo.views import MultiComplete
from todo.views import RepeatingList

urlpatterns = patterns('',
    url(r'^$', TemplateView.as_view(template_name="home.html"), name="home"),
    url(r'^todo$', TodoList.as_view(), name="list_tasks"),
    url(r'^user/(?P<slug>\w+[-\w\d]+)/$', UserView.as_view(), name="show_user"),
    url(r'^areas/', AreaList.as_view(), name="list_areas"),
    url(r'^area/(?P<slug>\w+[-\w\d]+)/$', AreaView.as_view(), name="show_area"),
    url(r'^lists/', ActionList.as_view(), name="list_actions"),
    url(r'^list/(?P<slug>\w+[-\w\d]+)/$', ActionView.as_view(), name="show_action"),
    url(r'^add/$', AddTask.as_view(), name="add_task"),
    url(r'^add/to/user/(?P<slug>\w+[-\w\d]+)/$', AddToUser.as_view(), name="add_to_user"),
    url(r'^add/to/list/(?P<slug>\w+[-\w\d]+)/$', AddToList.as_view(), name="add_to_list"),
    url(r'^add/to/area/(?P<slug>\w+[-\w\d]+)/$', AddToArea.as_view(), name="add_to_area"),
    url(r'^list/complete$', MultiComplete.as_view(), name='complete_multi'),
    url(r'^repeating/$', RepeatingList.as_view(), name='list_repeating'),
)
