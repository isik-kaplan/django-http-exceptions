from threading import local

from django.http import HttpResponse
from django.utils.deprecation import MiddlewareMixin

from .exceptions import HTTPExceptions


class ExceptionHandlerMiddleware(MiddlewareMixin):
    @staticmethod
    def process_exception(request, exc):
        if isinstance(exc, HTTPExceptions.BASE_EXCEPTION):
            response = getattr(exc, 'response', None)
            if not response and exc._has_default_view():
                response = exc._get_default_view_response(request)
            if not response:
                response = HttpResponse(content=exc.description.encode(), status=exc.status)
            return response


_thread_locals = local()


def get_current_request():
    return _thread_locals.request


class ThreadLocalRequestMiddleware(MiddlewareMixin):

    @staticmethod
    def process_request(request):
        _thread_locals.request = request

    @staticmethod
    def process_response(request, response):
        if hasattr(_thread_locals, 'request'):
            del _thread_locals.request
        return response

    @staticmethod
    def process_exception(request, exception):
        if hasattr(_thread_locals, 'request'):
            del _thread_locals.request
