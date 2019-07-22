from http import HTTPStatus

from django.http import HttpResponse


def _is_dunder(name):
    """Returns True if a __dunder__ name, False otherwise."""
    return (name[:2] == name[-2:] == '__' and
            name[2:3] != '_' and
            name[-3:-2] != '_' and
            len(name) > 4)


class transform(type):
    """@DynamicAttrs."""
    """A metaclass to help automatically apply a function to all 3rd party members of a class"""

    def __setattr__(self, key, value):
        return super().__setattr__(key, self.__transform__(value))

    @staticmethod
    def __raise_on_new(klass):
        """
        We don't want our transform types to be initilizable, they are only there to group together similiar items.
        """

        def __new__(cls, *a, **kw):
            raise TypeError('{} can not be initilazed.'.format(klass))

        return __new__

    def __new__(mcs, cls, bases, classdict):
        _transform = classdict['__transform__']
        _checks = classdict['__checks__']
        return type.__new__(
            mcs,
            cls,
            bases,
            {
                **{k: _transform(v) if _checks(k, v) else v
                   for k, v in classdict.items()},
                '__new__': mcs.__raise_on_new(cls)
            }
        )


class HTTPException(Exception):
    """@DynamicAttrs."""

    @classmethod
    def with_response(cls, response):
        exception = cls()
        response.status_code = exception.status
        exception.response = response
        return exception

    @classmethod
    def register_default_view(cls, view):
        cls._default_view = staticmethod(view)

    @classmethod
    def _has_default_view(cls):
        return getattr(cls, '_default_view')

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

    def __transform__(value):
        return type(
            value.name,
            (HTTPException,),
            {'__module__': 'HTTPExceptions', 'status': value.value, 'description': value.description}
        )

    def __checks__(key, value):
        return all((
            not _is_dunder(key),
            not callable(value),
            not isinstance(value, Exception),
            not isinstance(value, classmethod)
        ))

    @classmethod
    def from_status(cls, code):
        """Get the exception from status code"""
        return getattr(cls, HTTPStatus(code).name)

    # Add all possible HTTP status codes from http.HTTPStatus
    for status in list(HTTPStatus.__members__.values()):
        locals()[status.name] = status


