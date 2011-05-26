from django.conf.urls.defaults import *
from django.http import HttpResponseNotFound, HttpResponseServerError

urlpatterns = patterns('',
)

def _404(request):
    return HttpResponseNotFound('404 Page!')

def _500(request):
    return HttpResponseServerError('500 Page!')

handler404 = _404
handler500 = _500
