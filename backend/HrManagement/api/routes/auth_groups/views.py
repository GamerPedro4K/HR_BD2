from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import status
from django.db import connection
from rest_framework import serializers
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication
from api.utils.dotenv import is_debug_mode
from api.utils.permissions import check_permission_decorator
import json

class AuthGroupSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    name = serializers.CharField(max_length=100, required=True)

class AuthGroupViewSet(ViewSet):
    """
    ViewSet for managing auth groups.
    """
    serializer_class = AuthGroupSerializer
    
    if not is_debug_mode():
        authentication_classes = [JWTAuthentication]
        permission_classes = [IsAuthenticated]

    @check_permission_decorator('view_all_auth_groups')
    def list(self, request):
        """
        List all auth groups with their permissions.
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
                    FROM get_all_auth_groups(
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

                auth_groups = []
                total_count = rows[0][-1] if rows else 0

                for row in rows:
                    # Handle the case where permissions might be None
                    permissions = row[2] or []
                    # If permissions is a string, parse it
                    if isinstance(permissions, str):
                        try:
                            permissions = json.loads(permissions)
                        except json.JSONDecodeError:
                            permissions = []

                    auth_groups.append({
                        'id': row[0],
                        'name': row[1],
                        'permissions': permissions  # Now it will be a proper JSON array
                    })

                return Response({
                    'auth_groups': auth_groups,
                    'total_count': total_count
                }, status=status.HTTP_200_OK)

            except Exception as e:
                return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)


    @check_permission_decorator('view_auth_group')
    def retrieve(self, request, pk=None):
        """
        Retrieve a specific auth group by ID.
        """
        with connection.cursor() as cursor:
            try:
                query = """
                    SELECT 
                        ag.id,
                        ag.name,
                        jsonb_agg(
                            jsonb_build_object(
                                'id', ap.id,
                                'name', ap.name,
                                'codename', ap.codename,
                                'content_type', ct.app_label || '.' || ct.model
                            )
                        ) as permissions
                    FROM auth_group ag
                    LEFT JOIN auth_group_permissions agp ON ag.id = agp.group_id
                    LEFT JOIN auth_permission ap ON agp.permission_id = ap.id
                    LEFT JOIN django_content_type ct ON ap.content_type_id = ct.id
                    WHERE ag.id = %s
                    GROUP BY ag.id, ag.name
                """
                cursor.execute(query, [pk])
                row = cursor.fetchone()

                if not row:
                    return Response(
                        {'error': 'Auth group not found'}, 
                        status=status.HTTP_404_NOT_FOUND
                    )

                auth_group = {
                    'id': row[0],
                    'name': row[1],
                    'permissions': row[2]
                }

                return Response(auth_group, status=status.HTTP_200_OK)

            except Exception as e:
                return Response(
                    {'error': str(e)}, 
                    status=status.HTTP_400_BAD_REQUEST
                )

    @check_permission_decorator('create_auth_group')
    def create(self, request):
        serializer = self.serializer_class(data=request.data)

        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        data = serializer.validated_data

        with connection.cursor() as cursor:
            try:
                cursor.execute(
                    """
                    INSERT INTO auth_group (name)
                    VALUES (%s)
                    RETURNING id;
                    """,
                    [data['name']]
                )
                new_id = cursor.fetchone()[0]
            except Exception as e:
                return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)

        return Response({'message': 'Group created.', 'id': new_id}, status=status.HTTP_201_CREATED)

    @check_permission_decorator('update_auth_group')
    def update(self, request, pk=None):
        if not pk:
            return Response({'error': 'ID is required for updating a group.'},
                            status=status.HTTP_400_BAD_REQUEST)

        serializer = self.serializer_class(data=request.data)

        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        data = serializer.validated_data

        with connection.cursor() as cursor:
            try:
                cursor.execute(
                    """
                    UPDATE auth_group
                    SET name = %s
                    WHERE id = %s;
                    """,
                    [data['name'], pk]
                )
                if cursor.rowcount == 0:
                    return Response({'error': 'Group not found.'}, status=status.HTTP_404_NOT_FOUND)
            except Exception as e:
                return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)

        return Response({'message': 'Group updated successfully.'}, status=status.HTTP_200_OK)

    @check_permission_decorator('delete_auth_group')
    def destroy(self, request, pk=None):
        if not pk:
            return Response({'error': 'ID is required for deleting a group.'},
                            status=status.HTTP_400_BAD_REQUEST)

        with connection.cursor() as cursor:
            try:
                cursor.execute(
                    """
                    DELETE FROM auth_group
                    WHERE id = %s;
                    """,
                    [pk]
                )
                if cursor.rowcount == 0:
                    return Response({'error': 'Group not found.'}, status=status.HTTP_404_NOT_FOUND)
            except Exception as e:
                return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)

        return Response({'message': 'Group deleted successfully.'}, status=status.HTTP_200_OK)