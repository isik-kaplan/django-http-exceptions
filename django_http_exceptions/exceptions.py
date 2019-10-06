from http import HTTPStatus

from django.http import HttpResponse


def _is_dunder(name):
    """Returns True if a __dunder__ name, False otherwise."""
    return (name[:2] == name[-2:] == '__' and
            name[2:3] != '_' and
            name[-3:-2] != '_' and
            len(name) > 4)


class transform(type):
    """A metaclass to help automatically apply a function to all 3rd party members of a class

    @DynamicAttrs."""

    def __setattr__(self, key, value):
        return super().__setattr__(key, self.__transform__(value))

    @staticmethod
    def __raise_on_new(klass):
        """We don't want our transform types to be initilizable, they are only there to group
        together similiar items."""

        def __new__(cls, *a, **kw):
            raise TypeError('{} can not be initilazed.'.format(klass))

        return __new__

    @staticmethod
    def __noop_transform(key, value, classdict):
        return value

    @staticmethod
    def __noop_checks(key, value, classdict):
        return True

    def __new__(mcs, cls, bases, classdict):
        _transform = classdict.get('__transform__', mcs.__noop_transform)
        _checks = classdict.get('__checks__', mcs.__noop_checks)
        return type.__new__(
            mcs,
            cls,
            bases,
            {
                **{k: _transform(k, v, classdict) if _checks(k, v, classdict) else v
                   for k, v in classdict.items()},
                '__new__': mcs.__raise_on_new(cls)
            }
        )


class HTTPException(Exception):
    """@DynamicAttrs."""
    _error_handlers = []

    @classmethod
    def with_response(cls, response):
        exception = cls()
        response.status_code = exception.status
        exception.response = response
        return exception

    @classmethod
    def with_content(cls, content):
        exception = cls()
        exception.response = HttpResponse(content, status=exception.status)
        return exception

    @classmethod
    def register_default_view(cls, view):
        cls._default_view = staticmethod(view)

    @classmethod
    def register_error_handler(cls, handler):
        cls._error_handlers.append(handler)
        return handler

    @classmethod
    def remove_error_handler(cls, handler):
        cls._error_handlers.remove(handler)

    @classmethod
    def _has_default_view(cls):
        return hasattr(cls, '_default_view')

    @classmethod
    def _get_default_view_response(cls, request):
        response = cls._default_view(request)
        response.status_code = cls.status
        return response

    def __call__(self, *args):
        self.args += args
        return self


class HTTPExceptions(metaclass=transform):
    """@DynamicAttrs."""  # PycharmDisableInspection
    BASE_EXCEPTION = HTTPException
    encapsulated = ['exceptions', 'register_base_exception']
    exceptions = []

    def __transform__(key, value, classdict):
        base_exception = classdict.get('BASE_EXCEPTION') or HTTPException
        if not issubclass(base_exception, HTTPException):
            raise TypeError('BASE_EXCEPTION must be a subclass of HTTPException.')
        return type(
            value.name,
            (base_exception,),
            {'__module__': 'HTTPExceptions', 'status': value.value,
             'description': value.description}
        )

    def __checks__(key, value, classdict):
        return all((
            not _is_dunder(key),
            not callable(value),
            not isinstance(value, Exception),
            not isinstance(value, classmethod),
            key != 'encapsulated',
            key not in classdict.get('encapsulated', []),
        ))

    @classmethod
    def from_status(cls, code):
        """Get the exception from status code"""
        return getattr(cls, HTTPStatus(code).name)

    @classmethod
    def register_base_exception(cls, new_exception):
        for exception in cls.exceptions:
            if not issubclass(new_exception, HTTPException):
                raise TypeError('New exception must be a subclass of HTTPException.')
            getattr(cls, exception).__bases__ = (new_exception,)

    # Add all possible HTTP status codes from http.HTTPStatus
    for status in list(HTTPStatus.__members__.values()):
        locals()[status.name] = status
        exceptions.append(status.name)
