import pytz

from datetime import datetime

class LastRequestMiddleware:
    """
        Middleware used to update last_activity datetime field
        everytime user makes request to the server.
    """

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)
        if request.user.is_authenticated:
            request.user.last_activity = datetime.now().replace(tzinfo=pytz.UTC)
            request.user.save()

        return response