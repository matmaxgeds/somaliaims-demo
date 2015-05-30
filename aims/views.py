from django.shortcuts import redirect
from django.conf import settings


def login_success(request):
    """
    Redirects users based on whether they are in the admins group
    """
    if request.user.groups.filter(name="admin").exists() or request.user.is_superuser:
        # user is an admin
        return redirect(settings.ADMIN_URL)
    elif request.user.groups.filter(name="data").exists():
        return redirect(settings.DATA_ENTRY_URL)
    elif request.user.groups.filter(name="management").exists() or request.user.groups.filter(name="manager").exists():
        return redirect(settings.MANAGEMENT_URL)
    else:
        return redirect(settings.LOGIN_URL)