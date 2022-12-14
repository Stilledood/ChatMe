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

def custom_permission_required(permission):

    def decorator(cls):
        if not isinstance(cls,type) or not issubclass(cls,View):
            raise ImproperlyConfigured('custom permission required decorator must be apllied on View subclass')
        check_auth = method_decorator(login_required)
        check_perm = method_decorator(permission_required(permission,raise_exception=True))
        cls.dispatch = check_auth(check_perm(cls.dispatch))
        return cls
    return decorator
