from django import forms
from django.forms.forms import NON_FIELD_ERRORS


class ExForm(forms.Form):
    def add_error(self, message):
        if not self._errors:
            self._errors = forms.util.ErrorDict()
        if not NON_FIELD_ERRORS in self._errors:
            self._errors[NON_FIELD_ERRORS] = self.error_class()
        self._errors[NON_FIELD_ERRORS].append(message)


class LoginForm(ExForm):
    username = forms.CharField(label="User", required=True, max_length=32)
    password = forms.CharField(label="Password", required=True,
            widget=forms.PasswordInput)
