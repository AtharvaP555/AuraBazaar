import time
from collections import defaultdict
from django.http import HttpResponse


class RateLimitMiddleware:
    """
    Simple in-memory rate limiter.
    Limits POST requests to protected endpoints to 10 requests per minute per IP.
    """
    PROTECTED_PATHS = ['/shop/contact/', '/shop/checkout/', '/shop/tracker/']
    MAX_REQUESTS = 10
    WINDOW_SECONDS = 60

    def __init__(self, get_response):
        self.get_response = get_response
        self._requests = defaultdict(list)

    def __call__(self, request):
        if request.method == 'POST' and request.path in self.PROTECTED_PATHS:
            ip = self._get_ip(request)
            now = time.time()
            window_start = now - self.WINDOW_SECONDS

            # Drop timestamps outside the window
            self._requests[ip] = [
                t for t in self._requests[ip] if t > window_start
            ]

            if len(self._requests[ip]) >= self.MAX_REQUESTS:
                return HttpResponse(
                    'Too many requests. Please wait a minute and try again.',
                    status=429
                )

            self._requests[ip].append(now)

        return self.get_response(request)

    def _get_ip(self, request):
        forwarded = request.META.get('HTTP_X_FORWARDED_FOR')
        if forwarded:
            return forwarded.split(',')[0].strip()
        return request.META.get('REMOTE_ADDR', '0.0.0.0')