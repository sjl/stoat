from django.conf import settings
from django.http import Http404
from views import page


class StoatMiddleware(object):
    def process_response(self, request, response):
        if response.status_code != 404:
            # Pass anything but a 404 straight through.
            return response

        try:
            # Try the page view.
            return page(request, request.path_info)
        except Http404:
            # If the page view 404s, return the ORIGINAL 404 response.
            return response
        except:
            # If anything else happened, something is wrong with the page view.
            # Return the original (404) response, unless we're in DEBUG.
            if settings.DEBUG:
                raise
            return response
