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
        """
        List all departments along with their roles and associated training types.
        """
        
        with connection.cursor() as cursor:
            try:
                cursor.execute(
                    """
                    SELECT 
                        d.id_department, 
                        d.name AS department_name, 
                        d.description AS department_description,
                        r.id_role, 
                        r.role_name, 
                        r.hex_color, 
                        r.description AS role_description,
                        ttr.id_training_type, 
                        tt.name AS training_type_name,
                        tt.description AS training_type_description,
                        tt.hours AS training_type_hours
                    FROM 
                        departments d
                    LEFT JOIN 
                        roles r ON d.id_department = r.id_department
                    LEFT JOIN 
                        training_type_role ttr ON r.id_role = ttr.id_role
                    LEFT JOIN 
                        training_types tt ON ttr.id_training_type = tt.id_training_type
                    WHERE 
                        d.deleted_at IS NULL
                    ORDER BY 
                        d.name, r.role_name
                    """,
                )
                rows = cursor.fetchall()
            except Exception as e:
                return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)

        # Group roles and their training types under their respective departments
        departments = {}
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
            # Add training type information if it exists
            if row[7]:  # If training type exists
                departments[department_id]['roles'][role_id]['training_types'].append({
                    'id_training_type': row[7],
                    'name': row[8],
                    'description': row[9],
                    'hours': row[10],
                })

        # Convert roles dictionary to a list under each department
        for department in departments.values():
            department['roles'] = list(department['roles'].values())

        # Convert departments dictionary to a list for the response
        department_list = list(departments.values())

        return Response({'departments': department_list}, status=status.HTTP_200_OK)


    
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
