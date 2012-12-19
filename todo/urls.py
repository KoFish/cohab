from django.conf.urls import patterns, url  # , include
from django.views.generic import TemplateView
from todo.views import TodoList, AreaView, AreaList

urlpatterns = patterns('',
    url(r'^$', TemplateView.as_view(template_name="home.html"), name="home"),
    url(r'^todo$', TodoList.as_view(), name="list_tasks"),
    url(r'^areas/', AreaList.as_view(), name="list_areas"),
    url(r'^area/(?P<slug>\w+[-\w\d]+)/', AreaView.as_view(), name="show_area"),
)
