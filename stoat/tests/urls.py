from django.conf.urls.defaults import *
from django.http import HttpResponse, HttpResponseNotFound, HttpResponseServerError
from django.contrib import admin

admin.autodiscover()

def shadowed(request):
    return HttpResponse("This is a normal view.")

urlpatterns = patterns('',
    url(r'^admin/', include(admin.site.urls)),
    url(r'shadowed/$', shadowed)
)

def _404(request):
    return HttpResponseNotFound('404 Page!')

def _500(request):
    return HttpResponseServerError('500 Page!')

handler404 = _404
handler500 = _500
