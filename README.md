[![Build Status](https://travis-ci.com/isik-kaplan/django-http-exceptions.svg?branch=master)](https://travis-ci.com/isik-kaplan/django-http-exceptions)
[![codecov](https://codecov.io/gh/isik-kaplan/django-http-exceptions/branch/master/graph/badge.svg)](https://codecov.io/gh/isik-kaplan/django-http-exceptions) 
[![Python 3.5+](https://img.shields.io/badge/python-3.5+-brightgreen.svg)](#)
[![Django 2.0+](https://img.shields.io/badge/django-2.0+-brightgreen.svg)](#)
[![PyPI - License](https://img.shields.io/pypi/l/django-http-exceptions.svg)](https://pypi.org/project/django-http-exceptions/)
[![PyPI - Downloads](https://img.shields.io/pypi/dm/django-http-exceptions.svg)](https://pypi.org/project/django-http-exceptions/)


## What is *django-http-exceptions*?

It is raisable exceptions for your django views.



## What is it good for?

It makes this 

````py
def some_function():
    raise SomeError

def view(request):
   try:
       response = some_function()
   except SomeError:
       response = HttpResponse(status=403)
   return response
````
into this
````py
from django_http_exceptions import HTTPExceptions
def some_function():
    raise HTTPExceptions.FORBIDDEN # HTTPExceptions.from_status(403)

def view(request):
    return some_function() 
    
````

meaning that is saves you from boilerplate code. 

It also allows you to hook default views to **all possible http response codes**, meaning that you can use more than the 5-6 django provided error handlers.



## How to use it?

Just two middlewares, lower the better, and you are done.

````python
MIDDLEWARE = [
    ...,
    'django_http_exceptions.middleware.ExceptionHandlerMiddleware',
    'django_http_exceptions.middleware.ThreadLocalRequestMiddleware',
    ...
]
````

And that is it, you are ready to raise your http exceptions.



## What else? 


#### `HTTPExceptions`
Base class that provides all the exceptions to be raised.


#### `HTTPExceptions.from_status(status)`  
In case you don't want to write  
`HTTPExceptions.REQUEST_HEADER_FIELDS_TOO_LARGE`  
You can just write  
`HTTPExceptions.from_status(431)`


#### `HTTPExceptions.BASE_EXCEPTON`  
The base exception for all http exception

#### `HTTPExceptions.register_base_exception(exception)`
Given that `exception` is a class that inherits from `HTTPException` you can customize the exceptions.
Keep in mind that `HTTPException` is an `Exception` subclass itself.


#### `HTTPExceptions.BASE_EXCEPTION.with_response(response)`  
This is the method for raising exceptions with a response. You can put any response in this method while raising your
error.
 
Let's say you have a view named `index`, then this example would return what `index` function would return, but with
status code `410`  
`HTTPExceptions.GONE.with_response(index(request))`


#### `HTTPExceptions.BASE_EXCEPTION.with_content(content)`  
This method allow to raise an **HTTPException** with a custom message (can be either `str` or `bytes`).

For instance, `HTTPExceptions.NOT_FOUND.with_content("The user named 'username' could not be found")`
would return something equivalent to `HttpResponse("The user named 'username' could not be found", status=404)`.

#### `HTTPExceptions.BASE_EXCEPTION.with_json(json_data)`
This method allow to raise an **HTTPException** with a custom json response,  
`json_data` can be anything that `JsonResponse` accepts.

#### `HTTPExceptions.BASE_EXCEPTION.register_default_view(view)`  
`view` is a function that takes only one argument, `request` when you register a default view to an error class with
`HTTPExceptions.NOT_FOUND.register_defaul_view(view)`  when `HTTPExceptions.GONE` is raised it returns the view function, 
but again, with `404` status code. If the error has been raised with `.with_response`, that is used instead.   


#### `get_current_request`

This function gets you the current request anywhere in your django application, making it easier for your dynamic error 
responses to be created, like in the `HTTPExceptions.GONE.with_response(index(request))` example.
 
 
#### `ExceptionHandlerMiddleware` 

Just there for to exception handling to work.
 
 
#### `ThreadLocalRequestMiddleware` 
 
Just there for to `get_current_request` to work.


#### `errorify(error)`

Decorator that turns a view (both class and function) into an http error

````python
@errorify(HTTPExceptions.PAYMENT_REQUIRED)
class Subscribe(TemplateView):
    template = SUBSCRIBE_TEMPLATE
````

 
## Avaliable Exceptions
```py
HTTPExceptions.CONTINUE                              # HTTPExceptions.from_status(100)
HTTPExceptions.SWITCHING_PROTOCOLS                   # HTTPExceptions.from_status(101)
HTTPExceptions.PROCESSING                            # HTTPExceptions.from_status(102)
HTTPExceptions.OK                                    # HTTPExceptions.from_status(200)
HTTPExceptions.CREATED                               # HTTPExceptions.from_status(201)
HTTPExceptions.ACCEPTED                              # HTTPExceptions.from_status(202)
HTTPExceptions.NON_AUTHORITATIVE_INFORMATION         # HTTPExceptions.from_status(203)
HTTPExceptions.NO_CONTENT                            # HTTPExceptions.from_status(204)
HTTPExceptions.RESET_CONTENT                         # HTTPExceptions.from_status(205)
HTTPExceptions.PARTIAL_CONTENT                       # HTTPExceptions.from_status(206)
HTTPExceptions.MULTI_STATUS                          # HTTPExceptions.from_status(207)
HTTPExceptions.ALREADY_REPORTED                      # HTTPExceptions.from_status(208)
HTTPExceptions.IM_USED                               # HTTPExceptions.from_status(226)
HTTPExceptions.MULTIPLE_CHOICES                      # HTTPExceptions.from_status(300)
HTTPExceptions.MOVED_PERMANENTLY                     # HTTPExceptions.from_status(301)
HTTPExceptions.FOUND                                 # HTTPExceptions.from_status(302)
HTTPExceptions.SEE_OTHER                             # HTTPExceptions.from_status(303)
HTTPExceptions.NOT_MODIFIED                          # HTTPExceptions.from_status(304)
HTTPExceptions.USE_PROXY                             # HTTPExceptions.from_status(305)
HTTPExceptions.TEMPORARY_REDIRECT                    # HTTPExceptions.from_status(307)
HTTPExceptions.PERMANENT_REDIRECT                    # HTTPExceptions.from_status(308)
HTTPExceptions.BAD_REQUEST                           # HTTPExceptions.from_status(400)
HTTPExceptions.UNAUTHORIZED                          # HTTPExceptions.from_status(401)
HTTPExceptions.PAYMENT_REQUIRED                      # HTTPExceptions.from_status(402)
HTTPExceptions.FORBIDDEN                             # HTTPExceptions.from_status(403)
HTTPExceptions.NOT_FOUND                             # HTTPExceptions.from_status(404)
HTTPExceptions.METHOD_NOT_ALLOWED                    # HTTPExceptions.from_status(405)
HTTPExceptions.NOT_ACCEPTABLE                        # HTTPExceptions.from_status(406)
HTTPExceptions.PROXY_AUTHENTICATION_REQUIRED         # HTTPExceptions.from_status(407)
HTTPExceptions.REQUEST_TIMEOUT                       # HTTPExceptions.from_status(408)
HTTPExceptions.CONFLICT                              # HTTPExceptions.from_status(409)
HTTPExceptions.GONE                                  # HTTPExceptions.from_status(410)
HTTPExceptions.LENGTH_REQUIRED                       # HTTPExceptions.from_status(411)
HTTPExceptions.PRECONDITION_FAILED                   # HTTPExceptions.from_status(412)
HTTPExceptions.REQUEST_ENTITY_TOO_LARGE              # HTTPExceptions.from_status(413)
HTTPExceptions.REQUEST_URI_TOO_LONG                  # HTTPExceptions.from_status(414)
HTTPExceptions.UNSUPPORTED_MEDIA_TYPE                # HTTPExceptions.from_status(415)
HTTPExceptions.REQUESTED_RANGE_NOT_SATISFIABLE       # HTTPExceptions.from_status(416)
HTTPExceptions.EXPECTATION_FAILED                    # HTTPExceptions.from_status(417)
HTTPExceptions.UNPROCESSABLE_ENTITY                  # HTTPExceptions.from_status(422)
HTTPExceptions.LOCKED                                # HTTPExceptions.from_status(423)
HTTPExceptions.FAILED_DEPENDENCY                     # HTTPExceptions.from_status(424)
HTTPExceptions.UPGRADE_REQUIRED                      # HTTPExceptions.from_status(426)
HTTPExceptions.PRECONDITION_REQUIRED                 # HTTPExceptions.from_status(428)
HTTPExceptions.TOO_MANY_REQUESTS                     # HTTPExceptions.from_status(429)
HTTPExceptions.REQUEST_HEADER_FIELDS_TOO_LARGE       # HTTPExceptions.from_status(431)
HTTPExceptions.INTERNAL_SERVER_ERROR                 # HTTPExceptions.from_status(500)
HTTPExceptions.NOT_IMPLEMENTED                       # HTTPExceptions.from_status(501)
HTTPExceptions.BAD_GATEWAY                           # HTTPExceptions.from_status(502)
HTTPExceptions.SERVICE_UNAVAILABLE                   # HTTPExceptions.from_status(503)
HTTPExceptions.GATEWAY_TIMEOUT                       # HTTPExceptions.from_status(504)
HTTPExceptions.HTTP_VERSION_NOT_SUPPORTED            # HTTPExceptions.from_status(505)
HTTPExceptions.VARIANT_ALSO_NEGOTIATES               # HTTPExceptions.from_status(506)
HTTPExceptions.INSUFFICIENT_STORAGE                  # HTTPExceptions.from_status(507)
HTTPExceptions.LOOP_DETECTED                         # HTTPExceptions.from_status(508)
HTTPExceptions.NOT_EXTENDED                          # HTTPExceptions.from_status(510)
HTTPExceptions.NETWORK_AUTHENTICATION_REQUIRED       # HTTPExceptions.from_status(511)
```
