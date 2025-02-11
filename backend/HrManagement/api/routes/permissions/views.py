from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework import status
from api.utils.dotenv import is_debug_mode
from api.utils.permissions import check_permission_decorator
from django.db import connection
from rest_framework import serializers
from rest_framework.decorators import action

class GroupPermissionSerializer(serializers.Serializer):
    group_id = serializers.IntegerField(required=True)
    permission_ids = serializers.ListField(
        child=serializers.IntegerField(),
        required=True
    )
    
class PermissionsViewSet(ViewSet):
    
    if not is_debug_mode():
        authentication_classes = [JWTAuthentication]
        permission_classes = [IsAuthenticated]

    @check_permission_decorator('view_all_permissions')
    def list(self, request):
        """
        List all permissions with optional filtering and pagination.
        """
        order_by = request.GET.get('order_by', 'name')
        order_direction = request.GET.get('order_direction', 'ASC')
        global_search = request.GET.get('global_search', None)
        limit = request.GET.get('limit', None)
        offset = request.GET.get('offset', None)

        with connection.cursor() as cursor:
            try:
                limit = int(limit) if limit else None
                offset = int(offset) if offset else None

                query = """
                    SELECT *
                    FROM get_all_permissions(
                        %s::varchar,         -- global_search_param
                        ARRAY[%s]::text[],   -- order_by_param
                        ARRAY[%s]::text[],   -- order_direction_param
                        %s::integer,         -- limit_param
                        %s::integer          -- offset_param
                    )
                """
                params = [global_search, order_by, order_direction, limit, offset]

                cursor.execute(query, params)
                rows = cursor.fetchall()

                permissions = []
                total_count = rows[0][-1] if rows else 0

                for row in rows:
                    permissions.append({
                        'id': row[0],
                        'name': row[1],
                        'codename': row[2]
                    })

                return Response({
                    'permissions': permissions,
                    'total_count': total_count
                }, status=status.HTTP_200_OK)

            except Exception as e:
                return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)
            
    @check_permission_decorator('add_group_permissions')
    def create(self, request):
        """
        Add permissions to a group.
        
        Expected request data:
        {
            "group_id": 1,
            "permission_ids": [1, 2, 3]
        }
        """
        serializer = GroupPermissionSerializer(data=request.data)
        
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
            
        data = serializer.validated_data
        group_id = data['group_id']
        permission_ids = data['permission_ids']

        with connection.cursor() as cursor:
            try:
                # First verify if group exists
                cursor.execute(
                    "SELECT id FROM auth_group WHERE id = %s;",
                    [group_id]
                )
                if not cursor.fetchone():
                    return Response(
                        {'error': 'Group not found'},
                        status=status.HTTP_404_NOT_FOUND
                    )

                # Verify if all permissions exist
                placeholder = ','.join(['%s'] * len(permission_ids))
                cursor.execute(
                    f"SELECT id FROM auth_permission WHERE id IN ({placeholder});",
                    permission_ids
                )
                found_permissions = cursor.fetchall()
                if len(found_permissions) != len(permission_ids):
                    return Response(
                        {'error': 'One or more permissions not found'},
                        status=status.HTTP_404_NOT_FOUND
                    )

                # Add permissions to group
                for permission_id in permission_ids:
                    cursor.execute(
                        """
                        INSERT INTO auth_group_permissions (group_id, permission_id)
                        VALUES (%s, %s)
                        ON CONFLICT (group_id, permission_id) DO NOTHING;
                        """,
                        [group_id, permission_id]
                    )

                return Response(
                    {'message': 'Permissions added to group successfully'},
                    status=status.HTTP_200_OK
                )

            except Exception as e:
                return Response(
                    {'error': str(e)},
                    status=status.HTTP_400_BAD_REQUEST
                )

    @action(detail=False, methods=['post'])
    @check_permission_decorator('delete_group_permissions')
    def remove_permissions(self, request):
        """
        Remove permissions from a group.
        
        Expected request data:
        {
            "group_id": 1,
            "permission_ids": [1, 2, 3]
        }
        """
        serializer = GroupPermissionSerializer(data=request.data)
        
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
            
        data = serializer.validated_data
        group_id = data['group_id']
        permission_ids = data['permission_ids']

        with connection.cursor() as cursor:
            try:
                # First verify if group exists
                cursor.execute(
                    "SELECT id FROM auth_group WHERE id = %s;",
                    [group_id]
                )
                if not cursor.fetchone():
                    return Response(
                        {'error': 'Group not found'},
                        status=status.HTTP_404_NOT_FOUND
                    )

                # Remove permissions from group
                placeholder = ','.join(['%s'] * len(permission_ids))
                cursor.execute(
                    f"""
                    DELETE FROM auth_group_permissions
                    WHERE group_id = %s AND permission_id IN ({placeholder});
                    """,
                    [group_id] + permission_ids
                )

                return Response(
                    {'message': 'Permissions removed from group successfully'},
                    status=status.HTTP_200_OK
                )

            except Exception as e:
                return Response(
                    {'error': str(e)},
                    status=status.HTTP_400_BAD_REQUEST
                )