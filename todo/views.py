from django.views.generic import ListView, DetailView
from django.db.models import Q
from django.contrib.auth.models import User
from todo.models import Task, TaskArea, TaskAction
from lib.views import ProtectedMixin, AjaxMixin


class TodoList(ProtectedMixin, ListView):
    template_name = 'todo/list_todo.html'
    model = Task
    paginate_by = 10

    def get_context_data(self, *a, **kw):
        kw = super(TodoList, self).get_context_data(*a, **kw).copy()
        kw['other_users'] = User.objects.exclude(pk=self.request.user.pk)
        return kw

    def get_queryset(self):
        query = Q()
        if 'user' in self.request.GET:
            query &= Q(owner__pk=self.request.GET.get('user', None)) | Q(assigned__pk=self.request.GET.get('user', None))
        if 'completed' not in self.request.GET:
            query &= Q(completed__isnull=True)
        return Task.objects.filter(query)


class AreaList(ProtectedMixin, ListView):
    template_name = 'todo/list_areas.html'
    model = TaskArea
    paginate_by = 10

    def get_queryset(self):
        filters = {}
        if 'mine' in self.request.GET:
            filters['owner'] = self.request.user
        return TaskArea.objects.filter(**filters)


class AreaView(ProtectedMixin, AjaxMixin, DetailView):
    model = TaskArea
    template_name = 'todo/area_detail.html'
    ajax_template_name = 'todo/area_detail.stump.html'
    context_object_name = 'area'

    def get_context_data(self, *a, **kw):
        ret = super(AreaView, self).get_context_data(*a, **kw).copy()
        area = ret['area']
        ret['todo'] = area.tasks.filter(completed__isnull=True).all()
        ret['last'] = {}
        actions = TaskAction.objects.filter(tasks__area=area).select_related().distinct().all()
        for action in actions:
            tasks = action.tasks.filter(completed__isnull=False, area=area)
            if tasks.exists():
                ret['last'][action.name] = tasks.latest('completed')
        ret['other_users'] = User.objects.exclude(pk=self.request.user.pk)
        return ret
