import contextlib
import json
from http import HTTPStatus
from io import StringIO

from django.test import Client, SimpleTestCase

from django_http_exceptions import HTTPExceptions
from django_http_exceptions.exceptions import HTTPException

from . import views


class DjangoHTTPExceptionTestCase(SimpleTestCase):

    def setUp(self):
        self.client = Client()

    def test_from_status(self):
        for status in HTTPStatus:
            response = self.client.get("/from_status/%d/" % status.value)
            self.assertEqual(status.value, response.status_code)

    def test_from_name(self):
        for status in HTTPStatus:
            response = self.client.get("/from_name/%s/" % status.name)
            self.assertEqual(status.value, response.status_code)

    def test_with_response(self):
        response = self.client.get("/with_response/")
        self.assertContains(response, "It is indeed not found", status_code=404)

    def test_with_content(self):
        response = self.client.get("/with_content/")
        self.assertContains(response, "It is indeed not found", status_code=404)

    def test_with_json(self):
        response = self.client.get("/with_json/")
        response_json = response.json()
        self.assertJSONEqual(json.dumps(response_json), {"response_type": "json"})

    def test_register_default_view(self):
        HTTPExceptions.BAD_REQUEST.register_default_view(views.default_view)
        response = self.client.get("/from_status/400/")
        self.assertContains(response, "I am a default view", status_code=400)

    def test_errorify_function(self):
        response = self.client.get("/errorify/403/")
        self.assertEqual(403, response.status_code)

    def test_errorify_class(self):
        response = self.client.get("/errorify/404/")
        self.assertEqual(404, response.status_code)

    def test_does_not_catch_other_exception(self):
        with self.assertRaises(Exception):
            self.client.get("/exception/")

    def test_exceptions_can_be_subclassed(self):
        class CustomHTTPException(HTTPException):
            def __init__(self, *a, **kw):
                if a:
                    self.first_arg = a[0]
                super()

            @staticmethod
            def custom_static_method():
                return "STATIC METHOD"

            @classmethod
            def custom_class_method(cls):
                return "CLASS METHOD"

            def custom_method(self):
                return self.first_arg

        HTTPExceptions.register_base_exception(CustomHTTPException)

        self.assertEqual(HTTPExceptions.BAD_REQUEST.custom_static_method(), "STATIC METHOD")
        self.assertEqual(HTTPExceptions.BAD_REQUEST("first argument").custom_static_method(), "STATIC METHOD")
        self.assertEqual(HTTPExceptions.BAD_REQUEST.custom_class_method(), "CLASS METHOD")
        self.assertEqual(HTTPExceptions.BAD_REQUEST("first argument").custom_method(), "first argument")

    def test_require_HTTPException_as_base_class(self):
        class CustomHTTPException:
            def my_custom_method(self):
                return "YAY"

        with self.assertRaises(TypeError):
            HTTPExceptions.register_base_exception(CustomHTTPException)

    def test_error_handlers(self):

        @HTTPExceptions.NOT_FOUND.register_error_handler
        def handler(request, exc):
            print("404 logged")

        stdout = StringIO()
        with contextlib.redirect_stdout(stdout):
            self.client.get("/not_found/")

        self.assertEqual(stdout.getvalue().strip(), "404 logged")
        HTTPExceptions.NOT_FOUND.remove_error_handler(handler)

    def test_global_error_handler(self):

        @HTTPExceptions.BASE_EXCEPTION.register_error_handler
        def handler(request, exc):
            print("error logged")

        stdout = StringIO()
        with contextlib.redirect_stdout(stdout):
            self.client.get("/not_found/")

        self.assertEqual(stdout.getvalue().strip(), "error logged")
        HTTPExceptions.NOT_FOUND.remove_error_handler(handler)

    def test_global_and_single_error_handlers_together(self):

        @HTTPExceptions.BASE_EXCEPTION.register_error_handler
        def handler_global(request, exc):
            print("error logged")

        @HTTPExceptions.NOT_FOUND.register_error_handler
        def handler_404(request, exc):
            print("404 logged")

        stdout = StringIO()
        with contextlib.redirect_stdout(stdout):
            self.client.get("/not_found/")

        self.assertEqual(stdout.getvalue().strip(), "error logged\n404 logged")
        HTTPExceptions.NOT_FOUND.remove_error_handler(handler_404)
        HTTPExceptions.BASE_EXCEPTION.remove_error_handler(handler_global)
