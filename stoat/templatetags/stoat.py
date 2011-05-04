from django import template
from django.shortcuts import get_object_or_404
from django.http import Http404
from templatetag_sugar.parser import Name, Constant, Optional
from templatetag_sugar.register import tag

from .. import models

register = template.Library()

@tag(register, [Optional([Constant("as"), Name()])])
def current_page(context, asvar=None):
    url = context['request'].path_info.rstrip('/') + '/'
    try:
        page = get_object_or_404(models.Page, url__exact=url)
    except Http404:
        page = None

    if asvar:
        context[asvar] = page
    else:
        context['page'] = page

    return ''
