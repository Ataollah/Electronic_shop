# python
from appuser.models import PageVisit


class PageVisitMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)
        if request.method == 'GET':
            url = request.path
            if not (url.startswith('/static/') or url.startswith('/media/')):
                user = request.user if request.user.is_authenticated else None
                ip = request.META.get('REMOTE_ADDR')
                device = request.META.get('HTTP_USER_AGENT', '')
                PageVisit.objects.create(
                    user=user,
                    ip_address=None if user else ip,
                    device_info=device,
                    page_url=url
                )
        return response