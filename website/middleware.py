import re

from django.conf import settings
from django.contrib.auth.decorators import login_required

class RequireLoginMiddleware(object):
    def __init__(self):
        self.required = tuple([re.compile(url) for url in settings.LOGIN_REQUIRED_URLS])
        self.exceptions = tuple([re.compile(url) for url in settings.LOGIN_REQUIRED_URLS_EXCEPTIONS])

    def process_view(self,request,view_func,view_args,view_kwargs):
        # No need to process URLs if user already logged in
        if request.user.is_authenticated(): return None
        # An exception match should immediately return None
        for url in self.exceptions:
            if url.match(request.path): return None
            # Requests matching a restricted URL pattern are returned
        # wrapped with the login_required decorator
        for url in self.required:
            if url.match(request.path): return login_required(view_func)(request,*view_args,**view_kwargs)
            # Explicitly return None for all non-matching requests
        return None