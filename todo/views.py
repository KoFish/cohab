#from django import forms
from django.shortcuts import redirect
from django.views.generic import ListView, DetailView
from django.views.generic import TemplateView, View
from django.db.models import Q
from django.contrib.auth.models import User
from django.contrib import messages
from datetime import datetime
from todo.models import Task, TaskArea, TaskAction
from todo.exceptions import TodoCompletedException
from lib.views import ProtectedMixin, AjaxMixin


class TodoMixin(object):
    def get_context_data(self, *a, **kw):
        ctx = super(TodoMixin, self).get_context_data(*a, **kw)
        return ctx


class TodoList(ProtectedMixin, TodoMixin, ListView):
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


class UserView(ProtectedMixin, AjaxMixin, TodoMixin, DetailView):
    model = User
    template_name = 'todo/user_detail.html'
    ajax_template_name = 'todo/user_detail.stump.html'
    context_object_name = 'show_user'
    slug_field = 'username'

    def get_context_data(self, *a, **kw):
        ret = super(UserView, self).get_context_data(*a, **kw).copy()
        user = ret['show_user']
        ret['incomplete'] = user.tasks.filter(completed__isnull=True)
        ret['areas'] = user.areas.all()
        return ret


class AreaList(ProtectedMixin, TodoMixin, ListView):
    template_name = 'todo/list_areas.html'
    model = TaskArea
    paginate_by = 10

    def get_queryset(self):
        filters = {}
        if 'mine' in self.request.GET:
            filters['owner'] = self.request.user
        return TaskArea.objects.filter(**filters)


class AreaView(ProtectedMixin, AjaxMixin, TodoMixin, DetailView):
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


class ActionView(ProtectedMixin, AjaxMixin, TodoMixin, DetailView):
    model = TaskAction
    template_name = 'todo/action_detail.html'
    ajax_template_name = 'todo/action_detail.stump.html'
    context_object_name = 'action'

    def get_context_data(self, *a, **kw):
        ret = super(ActionView, self).get_context_data(*a, **kw).copy()
        action = ret['action']
        ret['todo'] = action.tasks.filter(completed__isnull=True)
        tasks = action.tasks.filter(completed__isnull=False)
        if tasks.exists():
            ret['last_tasks'] = tasks.order_by('object', '-completed').distinct('object')[:5]
        ret['other_users'] = User.objects.exclude(pk=self.request.user.pk)
        return ret


class ActionList(ProtectedMixin, TodoMixin, ListView):
    template_name = 'todo/list_actions.html'
    model = TaskAction
    paginate_by = 10

    def get_queryset(self):
        q = super(ActionList, self).get_queryset()
        filters = {"has_area": False, 'has_object': True}
        return q.filter(**filters)


class AddTask(ProtectedMixin, AjaxMixin, TodoMixin, TemplateView):
    template_name = 'todo/add_task.html'
    ajax_template_name = 'todo/add_task_form.html'

    def dispatch(self, request, *a, **kw):
        if not request.is_ajax():
            return redirect('todo:list_tasks')
        return super(AddTask, self).dispatch(request, *a, **kw)

    def get_context_data(self, *a, **kw):
        ctx = super(AddTask, self).get_context_data(*a, **kw)
        ctx['areas'] = TaskArea.objects.values('id', 'name')
        ctx['actions'] = TaskAction.objects.values('id', 'name', 'has_area', 'has_object')
        return ctx

    def post(self, request, *a, **kw):
        action = TaskAction.objects.get(id=request.POST.get('action'))
        deadline = request.POST.get('deadline', None)
        object_ = request.POST.get('object') if action.has_object else ""
        if action.has_object and not object_:
            return self.json_response({'status': 'error', 'message': 'This action needs an object'})
        t = {'deadline': datetime.strptime(deadline, "%Y/%m/%d") if deadline else None,
             'owner': request.user,
             'action': action,
             'object': object_,
             'area': TaskArea.objects.get(id=request.POST.get('area')) if action.has_area else None}
        if 'assign' in request.POST:
            t['assigned'] = User.objects.get(username=request.POST.get('assign'))
        Task.objects.create(**t)
        return self.json_response({'status': 'success'})


class AddToUser(AddTask):
    def get_context_data(self, *a, **kw):
        ctx = super(AddToUser, self).get_context_data(*a, **kw)
        ctx['assign'] = User.objects.get(username=self.kwargs['slug'])
        return ctx


class AddToArea(AddTask):
    def get_context_data(self, *a, **kw):
        ctx = super(AddTask, self).get_context_data(*a, **kw)
        ctx['area'] = TaskArea.objects.get(slug=self.kwargs['slug'])
        ctx['actions'] = TaskAction.objects.filter(has_area=True).values('id', 'name', 'has_area', 'has_object')
        return ctx


class AddToList(AddTask):
    def get_context_data(self, *a, **kw):
        ctx = super(AddTask, self).get_context_data(*a, **kw)
        ctx['areas'] = TaskArea.objects.values('id', 'name')
        ctx['action'] = TaskAction.objects.get(slug=self.kwargs['slug'])
        return ctx


class MultiComplete(ProtectedMixin, AjaxMixin, View):
    def post(self, request, *a, **kw):
        tasks = request.POST.getlist('complete')
        if tasks:
            print tasks
            for t in Task.objects.filter(pk__in=tasks).all():
                try:
                    t.complete(request)
                    messages.success(request, "%s has been set as completed" % t.name)
                except TodoCompletedException:
                    messages.warning(request, "%s has already been set as completed" % t.name)
        return self.json_response({'status': 'success'})
