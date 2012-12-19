from django.conf.urls import url
from tastypie.resources import ModelResource
from django.contrib.auth.models import User
from tastypie.http import HttpGone, HttpMultipleChoices
from django.core.exceptions import ObjectDoesNotExist, MultipleObjectsReturned


def is_action(f):
    def wrapper(*a, **kw):
        return f(*a, **kw)
    wrapper.is_action = True
    return wrapper


class ActionMixin(object):
    def base_urls(self):
        return [
            url(r"^(?P<resource_name>%s)/(?P<pk>\w[\w/-]*)/(?P<action>\w[\w/-]*)/(?P<arg>\w[\w/-]*)/$" % self._meta.resource_name, self.wrap_view('action_detail'), name="api_detail_action_with_arg"),
            url(r"^(?P<resource_name>%s)/(?P<pk>\w[\w/-]*)/(?P<action>\w[\w/-]*)$" % self._meta.resource_name, self.wrap_view('action_detail'), name="api_detail_action"),
        ] + super(ActionMixin, self).base_urls()

    def action_detail(self, request, **kwargs):
        kwargs = self.remove_api_resource_names(kwargs)
        action = kwargs.pop('action', None)
        arg = kwargs.pop('arg', None)
        try:
            obj = self.cached_obj_get(request=request, **kwargs)
        except ObjectDoesNotExist:
            return HttpGone()
        except MultipleObjectsReturned:
            return HttpMultipleChoices("More than one resource is found at "
                                       "this URI.")

        if hasattr(self, "action_%s" % action):
            f = getattr(self, "action_%s" % action)
            if f.is_action:
                if arg:
                    return f(request, obj, arg, **kwargs)
                else:
                    return f(request, obj, **kwargs)
            raise Exception("That is not an allowed action!")
        else:
            raise Exception("That's no action!")


class UserResource(ModelResource):
    class Meta:
        queryset = User.objects.all()
        allowed_methods = ['get']
        fields = ('username', 'first_name', 'last_name')
