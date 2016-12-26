from django.contrib.auth.decorators import user_passes_test
from django.utils.decorators import method_decorator


def class_decorator(function_decorator):
    """Convert a function based decorator into a class based decorator usable
    on class based Views.
    Can't subclass the `View` as it breaks inheritance (super in particular),
    so we monkey-patch instead.
    """
    def simple_decorator(View):
        View.dispatch = method_decorator(function_decorator)(View.dispatch)
        return View

    return simple_decorator

def group_required(*group_names, login_url=None):
    """Requires user membership in at least one of the groups passed in."""
    def in_groups(u):
        if u.is_authenticated():
            if bool(u.groups.filter(name__in=group_names)) | u.is_superuser:
                return True
        return False
    return user_passes_test(in_groups, login_url=login_url)
