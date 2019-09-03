from django.http import HttpResponse
from django.views import View

from django_http_exceptions import HTTPExceptions
from django_http_exceptions.utils import errorify


def from_status(_, status):
    raise HTTPExceptions.from_status(status)


def from_name(_, name):
    raise getattr(HTTPExceptions, name)


def with_response(_):
    raise HTTPExceptions.NOT_FOUND.with_response(HttpResponse("It is indeed not found"))


def with_content(_):
    raise HTTPExceptions.NOT_FOUND.with_content("It is indeed not found")


def exception(_):
    raise Exception


def default_view(_):
    return HttpResponse("I am a default view")


@errorify(HTTPExceptions.FORBIDDEN)
def errorify_403(_):
    return HttpResponse()


@errorify(HTTPExceptions.NOT_FOUND)
class Errorify404(View):

    def get(self, _):
        return HttpResponse()
