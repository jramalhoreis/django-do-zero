
from django.utils.decorators import method_decorator
from django.http import HttpResponseForbidden

def class_view_decorator(function_decorator):

    def decorator(view_object):
        view_object.dispatch = method_decorator(function_decorator)(view_object.dispatch)
        return view_object


    return decorator


def check_editor_access(view_function):

    def wrapper(request, *args, **kwargs):
        if request.user.groups.filter(name='Editor').exists():
            return view_function(request, *args, **kwargs)

        return HttpResponseForbidden('Voce não tem permissao para acessar este recurso')

    return wrapper


