from django.contrib.auth.models import User
from tastypie.authentication import MultiAuthentication, SessionAuthentication
from tastypie.authorization import DjangoAuthorization
from tastypie.resources import ModelResource, ALL, ALL_WITH_RELATIONS
from tastypie import fields
from todo.models import Task, TaskAction, TaskArea
from lib.resources import UserResource, ActionMixin, is_action


class TaskAreaResource(ModelResource):
    owner = fields.ToOneField(UserResource, 'owner', null=True)

    class Meta:
        queryset = TaskArea.objects.all()
        allowed_methods = ['get']
        filtering = {
            'owner': ALL_WITH_RELATIONS,
            'name': ALL
        }

        authentication = MultiAuthentication(SessionAuthentication())
        authorization = DjangoAuthorization()


class TaskActionResource(ModelResource):
    class Meta:
        queryset = TaskAction.objects.all()
        allowed_methods = ['get']
        filtering = {
            'name': ALL,
            'has_area': ALL
        }

        authentication = MultiAuthentication(SessionAuthentication())
        authorization = DjangoAuthorization()


class TaskResource(ActionMixin, ModelResource):
    owner = fields.ToOneField(UserResource, 'owner', null=True)
    assigned = fields.ToOneField(UserResource, 'assigned', null=True)
    action = fields.ToOneField(TaskActionResource, 'action', full=True)
    area = fields.ToOneField(TaskAreaResource, 'area', null=True, full=True)
    name = fields.CharField('name', readonly=True)

    class Meta:
        queryset = Task.objects.all()
        allowed_methods = ['get', 'post']
        filtering = {
            'owner': ALL_WITH_RELATIONS,
            'assigned': ALL_WITH_RELATIONS,
            'completedby': ALL_WITH_RELATIONS,
            'action': ALL_WITH_RELATIONS,
            'area': ALL_WITH_RELATIONS,
            'object': ALL,
            'added': ['gt', 'gte', 'lte', 'lt', 'range'],
            'deadline': ['isnull', 'gt', 'gte', 'lte', 'lt', 'range'],
            'completed': ['isnull', 'gt', 'gte', 'lte', 'lt', 'range'],
        }

        authentication = MultiAuthentication(SessionAuthentication())
        authorization = DjangoAuthorization()

    @is_action
    def action_complete(self, request, obj, **kw):
        task_resource = TaskResource()
        obj.complete(request)
        return task_resource.get_detail(request, pk=obj.pk)

    @is_action
    def action_claim(self, request, obj, **kw):
        task_resource = TaskResource()
        obj.claim(request)
        return task_resource.get_detail(request, pk=obj.pk)

    @is_action
    def action_assign(self, request, obj, arg, **kw):
        task_resource = TaskResource()
        user = User.objects.get(username=arg)
        obj.assign_to(user)
        return task_resource.get_detail(request, pk=obj.pk)

    @is_action
    def action_owner(self, request, obj, **kw):
        user_resource = UserResource()
        return user_resource.get_detail(request, pk=obj.owner.pk)
