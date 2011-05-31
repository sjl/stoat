# {{{
from django.conf import settings
from django.http import Http404, HttpResponsePermanentRedirect, HttpResponseBadRequest
from django.shortcuts import get_object_or_404, render_to_response
from django.template import RequestContext
from django.views.decorators.csrf import csrf_protect

from forms import MovePageForm
from models import Page
from stemplates import get_path
# }}}


def page(request, url):
    if not url.startswith('/'):
        url = "/" + url
    try:
        p = get_object_or_404(Page, url__exact=url)
    except Http404:
        if not url.endswith('/') and settings.APPEND_SLASH:
            new_url = url + "/"
            get_object_or_404(Page, url__exact=new_url)
            return HttpResponsePermanentRedirect("%s/" % request.path)
        else:
            raise
    return render_page(request, p)

@csrf_protect
def render_page(request, p):
    return render_to_response(get_path(p.template), {
        'page': p,
    }, context_instance=RequestContext(request))


def move_page(request):
    if not request.POST:
        return HttpResponseBadRequest()

    form = MovePageForm(request.POST)
    if form.is_valid():
        page = form.cleaned_data['page']
        page_id = page.id
        target = form.cleaned_data['target']
        position = form.cleaned_data['position']

        page._clear_ancestor_caches()
        if position == 'above':
            page.move(target, 'left')
        elif position == 'below':
            page.move(target, 'right')
        elif position == 'inside':
            page.move(target, 'last-child')

        page = Page.objects.get(id=page_id)
        page.save()

    # TODO: Make this dynamic.
    return HttpResponsePermanentRedirect('/admin/stoat/page/')

