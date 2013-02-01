from django import forms
from lib.forms import ErrorMixin
from todo.models import Task


class TaskForm(ErrorMixin, forms.ModelForm):
    deadline = forms.DateTimeField(widget=forms.TextInput(attrs={'class': "jdpicker"}))

    class Meta:
        model = Task
        exclude = ('owner', 'assigned', 'completedby', 'completed')
