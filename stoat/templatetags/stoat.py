# {{{
import random

from django import template
from django.core.cache import cache
from django.http import Http404
from django.shortcuts import get_object_or_404
from templatetag_sugar.parser import Name, Constant, Optional
from templatetag_sugar.register import tag

from .. import models


register = template.Library()
# }}}

def _get_roots():
    return list(models.Page.objects.filter(depth=1, show_in_nav=True))

def _get_roots_and_children(roots):
    results = []
    child_ids = set()
    for root in roots:
        key = 'stoat:pages:%d:children' % (root.id)
        ids = cache.get(key)
        if ids == None:
            ids = [c.id for c in root.get_children().filter(show_in_nav=True)]
            cache.set(key, ids, random.randint(300, 360))

        child_ids = child_ids.union(ids)
        results.append([root, ids])

    children = dict([(child.id, child)
                    for child in models.Page.objects.filter(id__in=child_ids)])
    for result in results:
        result[1] = [children[id] for id in result[1]]

    return results


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


@tag(register, [Optional([Constant("as"), Name()])])
def nav_roots(context, asvar=None):
    roots = _get_roots()

    if asvar:
        context[asvar] = roots
    else:
        context['nav'] = roots

    return ''


@tag(register, [Optional([Constant("as"), Name()])])
def nav_roots_and_children(context, asvar=None):
    roots = _get_roots()
    results = _get_roots_and_children(roots)

    if asvar:
        context[asvar] = results
    else:
        context['nav'] = results

    return ''

