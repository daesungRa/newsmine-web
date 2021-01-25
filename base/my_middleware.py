from django.http import Http404
from django.contrib import messages


def admin_restriction_middleware(get_response):
    def middleware(request):
        request_uri = request.META.get('PATH_INFO', None)
        if request_uri:
            split_request_uri = request_uri.split('/')
            # User access check for '/admin'
            if split_request_uri[1] == 'admin' and not request.user.is_staff:
                messages.add_message(request, messages.WARNING, f"Can't find this page -> '{request_uri}'")
                raise Http404(f"Can't find this page -> '{request_uri}'")
        response = get_response(request)
        return response
    return middleware
