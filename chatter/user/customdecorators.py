from django.views.generic import View
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required,permission_required
from django.core.exceptions import ImproperlyConfigured


def custom_login_decorator(cls):
    if not isinstance(cls,type) or not issubclass(cls,View):
        raise ImproperlyConfigured('custom login decorator must be aplied to a View subclass')
    decorator = method_decorator(login_required())
    cls.dispatch = decorator(cls.dispatch)
    return cls