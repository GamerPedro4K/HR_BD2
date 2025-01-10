from functools import wraps
from rest_framework.response import Response
from rest_framework import status
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth.models import Permission
from api.utils.dotenv import is_debug_mode 

def check_permission(user, permission_codename):
    if not is_debug_mode():
        """
        Checks if the user has a specific permission by codename.
        If the user lacks the permission, returns a Response object with a 403 error.

        Args:
            user (User): The user object to check permissions for.
            permission_codename (str): The codename of the permission to check (ignores app label).

        Returns:
            Response | None: Returns a 403 Response if the user lacks the permission; otherwise, None.
        """
        # Refresh user to ensure permissions are up-to-date
        user.refresh_from_db()

        # Fetch all permissions directly
        permissions = user.get_all_permissions()

        # Check if the user has the specific permission
        has_permission = f"{permission_codename}" in [perm.split('.')[-1] for perm in permissions]
        
        if not has_permission:
            return Response(
                {"error": f"Você não tem a permissão necessária: '{permission_codename}'."},
                status=status.HTTP_403_FORBIDDEN
            )

    return None



def check_permission_decorator(permission_codename):
    
    def decorator(view_func):
        @wraps(view_func)
        def _wrapped_view(self, request, *args, **kwargs):
            response = check_permission(request.user, permission_codename)
            if response:
                return response
            else:
                return view_func(self, request, *args, **kwargs)
        return _wrapped_view
    return decorator
