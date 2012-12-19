from django.template import Node, resolve_variable
from django.template import Variable
from django.core.urlresolvers import reverse
from django import template

register = template.Library()


@register.simple_tag
def api_detail_action(resource_name, pk, action):
    if ':' in resource_name:
        namespace, resource_name = resource_name.split(':', 1)
    else:
        namespace = None
    if '.' in resource_name:
        api_name, resource_name = resource_name.split('.', 1)
    else:
        api_name = 'v1'
    return reverse((namespace + ':' if namespace else '') + 'api_detail_action', kwargs={
        'api_name': api_name,
        'resource_name': resource_name,
        'pk': pk,
        'action': action})

@register.simple_tag
def api_detail_action_with_arg(resource_name, pk, arg, action):
    if ':' in resource_name:
        namespace, resource_name = resource_name.split(':', 1)
    else:
        namespace = None
    if '.' in resource_name:
        api_name, resource_name = resource_name.split('.', 1)
    else:
        api_name = 'v1'
    return reverse((namespace + ':' if namespace else '') + 'api_detail_action_with_arg', kwargs={
        'api_name': api_name,
        'resource_name': resource_name,
        'arg': arg,
        'pk': pk,
        'action': action})

"""
{% load add_get_parameter %}
<a href="{% add_get_paramater param1='const_value',param2=variable_in_context %}">
    Link with modified params
</a>

URL: http://django.mar.lt/2010/07/add-get-parameter-tag.html
"""


class AddGetParameter(Node):
    def __init__(self, values):
        self.values = values

    def render(self, context):
        req = resolve_variable('request', context)
        params = req.GET.copy()
        for key, value in self.values.items():
            params[key] = Variable(value).resolve(context)
        return '?%s' % params.urlencode()


@register.tag
def add_to_get(parser, token):
    from re import split
    contents = split(r'\s+', token.contents, 2)[1]
    pairs = split(r',', contents)
    values = {}
    for pair in pairs:
        s = split(r'=', pair, 2)
        values[s[0]] = s[1]

    return AddGetParameter(values)
