from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

class UserPermissionsViewSet(ViewSet):
    permission_classes = [IsAuthenticated]

    def list(self, request):
        """
        List all permissions for the authenticated user.
        """
        permissions = [perm.split('.', 1)[-1] for perm in request.user.get_all_permissions()]
        return Response({"permissions": permissions})
