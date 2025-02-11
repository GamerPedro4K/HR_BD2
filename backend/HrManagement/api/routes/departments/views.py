from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import status
from django.db import connection
from rest_framework import serializers
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication
from api.utils.dotenv import is_debug_mode 
from api.utils.permissions import check_permission_decorator

class DepartmentSerializer(serializers.Serializer):
    id_department = serializers.UUIDField(read_only=True)
    name = serializers.CharField(max_length=100, required=True)
    description = serializers.CharField(required=False, allow_blank=True)

class DepartmentViewSet(ViewSet):
    """
    ViewSet for managing departments.
    """
    serializer_class = DepartmentSerializer
    
    if not is_debug_mode():
        authentication_classes = [JWTAuthentication]
        permission_classes = [IsAuthenticated]
        

    @check_permission_decorator('view_all_departments')
    def list(self, request):
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
                    FROM get_all_departments(
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

                departments = {}
                total_count = rows[0][-1] if rows else 0

                for row in rows:
                    department_id = row[0]
                    if department_id not in departments:
                        departments[department_id] = {
                            'id_department': row[0],
                            'name': row[1],
                            'description': row[2],
                            'roles': {}
                        }

                    role_id = row[3]
                    if role_id and role_id not in departments[department_id]['roles']:
                        departments[department_id]['roles'][role_id] = {
                            'id_role': row[3],
                            'role_name': row[4],
                            'hex_color': row[5],
                            'description': row[6],
                            'training_types': []
                        }

                    if row[7]:  # If training type exists
                        departments[department_id]['roles'][role_id]['training_types'].append({
                            'id_training_type': row[7],
                            'name': row[8],
                            'description': row[9],
                            'hours': row[10]
                        })

                for department in departments.values():
                    department['roles'] = list(department['roles'].values())

                department_list = list(departments.values())

                return Response({
                    'departments': department_list,
                    'total_count': total_count
                }, status=status.HTTP_200_OK)

            except Exception as e:
                return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)

        
    @check_permission_decorator('view_department')
    def retrieve(self, request, pk=None):
        """
        Retrieve a single department by ID.
        """
        with connection.cursor() as cursor:
            try:
                cursor.execute(
                    """
                    SELECT id_department, name, description
                    FROM departments
                    WHERE id_department = %s;
                    """,
                    [pk]
                )
                row = cursor.fetchone()
            except Exception as e:
                return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)

        if not row:
            return Response({'error': 'Department not found.'}, status=status.HTTP_404_NOT_FOUND)

        department = {
            'id_department': row[0],
            'name': row[1],
            'description': row[2],
        }
        return Response(department, status=status.HTTP_200_OK)

    
    @check_permission_decorator('create_department')
    def create(self, request):
        """
        Create a new department.
        """
        serializer = self.serializer_class(data=request.data)

        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        data = serializer.validated_data

        with connection.cursor() as cursor:
            try:
                cursor.execute(
                    """
                    INSERT INTO departments (name, description)
                    VALUES (%s, %s)
                    RETURNING id_department;
                    """,
                    [data['name'], data.get('description')]
                )
                new_id = cursor.fetchone()[0]
            except Exception as e:
                return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)

        return Response({'message': 'Department created.', 'id_department': new_id}, status=status.HTTP_201_CREATED)

    
    @check_permission_decorator('update_department')
    def update(self, request, pk=None):
        """
        Update a department by ID.
        """
        if not pk:
            return Response({'error': 'ID (pk) is required for updating a department.'},
                            status=status.HTTP_400_BAD_REQUEST)

        serializer = self.serializer_class(data=request.data)

        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        data = serializer.validated_data

        with connection.cursor() as cursor:
            try:
                cursor.execute(
                    """
                    UPDATE departments
                    SET name = %s, description = %s, updated_at = NOW()
                    WHERE id_department = %s;
                    """,
                    [data['name'], data.get('description'), pk]
                )
                if cursor.rowcount == 0:
                    return Response({'error': 'Department not found.'}, status=status.HTTP_404_NOT_FOUND)
            except Exception as e:
                return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)

        return Response({'message': 'Department updated successfully.'}, status=status.HTTP_200_OK)
    
    
    @check_permission_decorator('delete_department')
    def destroy(self, request, pk=None):
        """
        Delete a department by ID.
        """
        if not pk:
            return Response({'error': 'ID (pk) is required for deleting a department.'},
                            status=status.HTTP_400_BAD_REQUEST)

        with connection.cursor() as cursor:
            try:
                cursor.execute(
                    """
                    DELETE FROM departments
                    WHERE id_department = %s;
                    """,
                    [pk]
                )
                if cursor.rowcount == 0:
                    return Response({'error': 'Department not found.'}, status=status.HTTP_404_NOT_FOUND)
            except Exception as e:
                return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)

        return Response({'message': 'Department deleted successfully.'}, status=status.HTTP_200_OK)
