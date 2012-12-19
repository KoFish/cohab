from django.views.generic import FormView, RedirectView
from django.core.exceptions import ImproperlyConfigured
from django.contrib import auth
from django.contrib.auth.decorators import login_required
from lib.forms import LoginForm
from django.utils import simplejson as json
from django.utils.decorators import method_decorator
from django import http


class ProtectedMixin(object):
    @method_decorator(login_required)
    def dispatch(self, *a, **kw):
        return super(ProtectedMixin, self).dispatch(*a, **kw)


class AjaxMixin(object):
    ajax_template_name = None

    def get_template_names(self):
        if self.request.is_ajax():
            if self.ajax_template_name is None:
                raise ImproperlyConfigured(
                        "Missing 'ajax_template_name' alternative template.")
            else:
                return [self.ajax_template_name] +\
                            super(AjaxMixin, self).get_template_names()
        return super(AjaxMixin, self).get_template_names()

    def json_response(self, content, **kw):
        return http.HttpResponse(json.dumps(content),
                content_type='application/json',
                **kw)

    def get_json_context(self, *a, **kw):
        return {}

    def form_valid(self, form):
        if self.request.is_ajax():
            return self.json_response(dict({
                'status': 'success',
                'redirect': self.get_success_url()},
                **self.get_json_context(form)))
        else:
            return super(AjaxMixin, self).form_valid(form)


class LoginView(AjaxMixin, FormView):
    template_name = "login.html"
    ajax_template_name = "login_form.html"
    form_class = LoginForm

    def get_success_url(self):
        return self.request.GET.get('next', '/')

    def form_valid(self, form):
        username = form.cleaned_data['username']
        password = form.cleaned_data['password']
        user = auth.authenticate(username=username, password=password)
        if user is not None and user.is_active:
            auth.login(self.request, user)
            return super(LoginView, self).form_valid(form)
        else:
            form.add_error("Incorrect credentials or inactive user")
            return self.form_invalid(form)


class LogoutView(RedirectView):
    def get(self, *a, **kw):
        auth.logout(self.request)
        print "Stuff"
        return super(LogoutView, self).get(*a, **kw)

    def get_redirect_url(self):
        print "Redirect url"
        return self.request.GET.get('next', '/')
