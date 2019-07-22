from http import HTTPStatus

from django.test import Client, SimpleTestCase

from django_http_exceptions import HTTPExceptions
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
