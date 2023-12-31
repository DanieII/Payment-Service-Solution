from django.shortcuts import redirect


class AlwaysRequireAccountMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if (
                not (request.path.startswith("/authentication/") or request.path.startswith("/webhooks/"))
                and not request.user.is_authenticated
        ):
            return redirect("login")

        response = self.get_response(request)
        return response
