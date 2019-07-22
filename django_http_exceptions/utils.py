import functools

from django.utils.decorators import method_decorator


def errorify(error):
    def decorator(view):
        if isinstance(view, type):
            return _errorify_class(view, error)
        else:
            return _errorify_function(view, error)

    return decorator


def _errorify_class(cls, error):
    return method_decorator(
        functools.partial(_errorify_function, error=error), name='dispatch'
    )(cls)


def _errorify_function(f, error):
    @functools.wraps(f)
    def inner(*a, **kw):
        raise error.with_response(f(*a, **kw))

    return inner
