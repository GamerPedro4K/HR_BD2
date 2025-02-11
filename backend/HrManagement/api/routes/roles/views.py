from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import status
from django.db import connection
from rest_framework import serializers
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication
from api.utils.dotenv import is_debug_mode 
from api.utils.permissions import check_permission_decorator

class RoleSerializer(serializers.Serializer):
    id_role = serializers.UUIDField(read_only=True)
    id_department = serializers.UUIDField(required=False)
    id_auth_group = serializers.IntegerField(required=True)
    role_name = serializers.CharField(max_length=100, required=True)
    hex_color = serializers.CharField(max_length=7, required=False, allow_blank=True)
    description = serializers.CharField(required=False, allow_blank=True)

class RolesViewSet(ViewSet):
    """
    ViewSet for managing roles.
    """
    serializer_class = RoleSerializer
    
    if not is_debug_mode():
        authentication_classes = [JWTAuthentication]
        permission_classes = [IsAuthenticated]

    @check_permission_decorator('view_all_roles')
    def list(self, request):
        """
        List all roles with optional filtering and pagination.
        """
        order_by = request.GET.get('order_by', 'role_name')
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
                    FROM get_all_roles(
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

                roles_dict = {}
                total_count = rows[0][-1] if rows else 0

                for row in rows:
                    role_id = row[0]  # id_role is the first column
                    
                    if role_id not in roles_dict:
                        roles_dict[role_id] = {
                            'id_role': row[0],
                            'id_department': row[1],
                            'id_auth_group': row[2],
                            'role_name': row[3],
                            'hex_color': row[4],
                            'description': row[5],
                            'department_name': row[6],
                            'training_types': []
                        }
                    
                    # Add training type if it exists and is not null
                    if row[7]:  # id_training_type is not null
                        training_type = {
                            'id_training_type': row[7],
                            'name': row[8],
                            'description': row[9],
                            'hours': row[10]
                        }
                        # Check if training type is not already in the list
                        if not any(tt['id_training_type'] == training_type['id_training_type'] 
                                 for tt in roles_dict[role_id]['training_types']):
                            roles_dict[role_id]['training_types'].append(training_type)

                # Convert dictionary to list
                roles = list(roles_dict.values())

                return Response({
                    'roles': roles,
                    'total_count': total_count
                }, status=status.HTTP_200_OK)

            except Exception as e:
                return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)

    @check_permission_decorator('view_role')
    def retrieve(self, request, pk=None):
        """
        Retrieve a single role by ID.
        """
        with connection.cursor() as cursor:
            try:
                cursor.execute(
                    """
                    SELECT r.id_role, r.id_department, r.id_auth_group, r.role_name, r.hex_color, r.description, 
                        d.name as department_name,
                        COALESCE(
                            json_agg(
                                json_build_object(
                                    'id_training_type', tt.id_training_type,
                                    'name', tt.name,
                                    'description', tt.description,
                                    'hours', tt.hours
                                )
                            ) FILTER (WHERE tt.id_training_type IS NOT NULL),
                            '[]'::json
                        ) as training_types
                    FROM roles r
                    JOIN departments d ON r.id_department = d.id_department
                    LEFT JOIN training_type_role ttr ON r.id_role = ttr.id_role AND ttr.deleted_at IS NULL
                    LEFT JOIN training_types tt ON ttr.id_training_type = tt.id_training_type AND tt.deleted_at IS NULL
                    WHERE r.id_role = %s
                    GROUP BY r.id_role, r.id_department, r.id_auth_group, r.role_name, r.hex_color, r.description, d.name;
                    """,
                    [pk]
                )
                row = cursor.fetchone()
            except Exception as e:
                return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)

        if not row:
            return Response({'error': 'Role not found.'}, status=status.HTTP_404_NOT_FOUND)

        role = {
            'id_role': row[0],
            'id_department': row[1],
            'id_auth_group': row[2],
            'role_name': row[3],
            'hex_color': row[4],
            'description': row[5],
            'department_name': row[6],
            'training_types': row[7]
        }
        return Response(role, status=status.HTTP_200_OK)

    @check_permission_decorator('create_role')
    def create(self, request):
        """
        Create a new role.
        """
        serializer = self.serializer_class(data=request.data)

        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        data = serializer.validated_data
        training_types = request.data.get('training_types', [])

        with connection.cursor() as cursor:
            try:
                cursor.execute(
                    """
                    INSERT INTO roles (id_department, id_auth_group, role_name, hex_color, description)
                    VALUES (%s, %s, %s, %s, %s)
                    RETURNING id_role;
                    """,
                    [
                        data['id_department'],
                        data['id_auth_group'],
                        data['role_name'],
                        data.get('hex_color'),
                        data.get('description')
                    ]
                )
                new_id = cursor.fetchone()[0]
                
                 # Insert training type associations
                if training_types:
                    values = [(tt, new_id) for tt in training_types]
                    cursor.executemany(
                        """
                        INSERT INTO training_type_role (id_training_type, id_role)
                        VALUES (%s, %s)
                        """,
                        values
                    )
            except Exception as e:
                return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)

        return Response({
            'message': 'Role created successfully.',
            'id_role': new_id
        }, status=status.HTTP_201_CREATED)

    @check_permission_decorator('update_role')
    def update(self, request, pk=None):
        """
        Update a role by ID.
        """
        if not pk:
            return Response(
                {'error': 'ID (pk) is required for updating a role.'},
                status=status.HTTP_400_BAD_REQUEST
            )

        serializer = self.serializer_class(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        data = serializer.validated_data
        training_types = request.data.get('training_types', [])

        with connection.cursor() as cursor:
            try:
                # Delete all existing training types for this role
                cursor.execute(
                    """
                    DELETE FROM training_type_role
                    WHERE id_role = %s;
                    """,
                    [pk]
                )

                # Insert new training types
                if training_types:
                    values = [(tt, pk) for tt in training_types]
                    cursor.executemany(
                        """
                        INSERT INTO training_type_role (id_training_type, id_role)
                        VALUES (%s, %s)
                        """,
                        values
                    )

                # Update role
                cursor.execute(
                    """
                    UPDATE roles
                    SET 
                        id_auth_group = %s,
                        role_name = %s,
                        hex_color = %s,
                        description = %s,
                        updated_at = NOW()
                    WHERE id_role = %s;
                    """,
                    [
                        data['id_auth_group'],
                        data['role_name'],
                        data.get('hex_color'),
                        data.get('description'),
                        pk
                    ]
                )
                if cursor.rowcount == 0:
                    return Response({'error': 'Role not found.'}, status=status.HTTP_404_NOT_FOUND)
            except Exception as e:
                return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)

        return Response({'message': 'Role updated successfully.'}, status=status.HTTP_200_OK)

    @check_permission_decorator('delete_role')
    def destroy(self, request, pk=None):
        """
        Delete a role by ID.
        """
        if not pk:
            return Response(
                {'error': 'ID (pk) is required for deleting a role.'},
                status=status.HTTP_400_BAD_REQUEST
            )

        with connection.cursor() as cursor:
            try:
                cursor.execute(
                    """
                    UPDATE roles 
                    SET deleted_at = NOW() 
                    WHERE id_role = %s;
                    """,
                    [pk]
                )
                if cursor.rowcount == 0:
                    return Response({'error': 'Role not found.'}, status=status.HTTP_404_NOT_FOUND)
            except Exception as e:
                return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)

        return Response({'message': 'Role deleted successfully.'}, status=status.HTTP_200_OK)