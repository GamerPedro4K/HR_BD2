from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import status
from django.db import connection
from rest_framework import serializers
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication
from api.utils.dotenv import is_debug_mode 
from api.utils.permissions import check_permission_decorator

class TrainingTypeSerializer(serializers.Serializer):
    id_training_type = serializers.UUIDField(read_only=True)
    name = serializers.CharField(max_length=50, required=True)
    description = serializers.CharField(required=True)
    hours = serializers.IntegerField(required=False, allow_null=True)


class TrainingTypeViewSet(ViewSet):
    """
    ViewSet for managing training types.
    """
    serializer_class = TrainingTypeSerializer
    
    if not is_debug_mode():
        authentication_classes = [JWTAuthentication]
        permission_classes = [IsAuthenticated]
        

    @check_permission_decorator('view_all_training_types')
    def list(self, request):
        """
        List all training types with optional filtering and pagination.
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
                    FROM get_all_training_types(
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

                training_types = []
                total_count = rows[0][-1] if rows else 0  # O último campo é o total_count

                for row in rows:
                    training_types.append({
                        'id_training_type': row[0],
                        'name': row[1],
                        'description': row[2],
                        'hours': row[3]
                    })

                return Response({
                    'training_types': training_types,
                    'total_count': total_count
                }, status=status.HTTP_200_OK)

            except Exception as e:
                return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)


    
    @check_permission_decorator('view_training_type')
    def retrieve(self, request, pk=None):
        """
        Retrieve a single training type by ID.
        """
        with connection.cursor() as cursor:
            try:
                cursor.execute(
                    """
                    SELECT id_training_type, name, description, hours
                    FROM training_types
                    WHERE id_training_type = %s;
                    """,
                    [pk]
                )
                row = cursor.fetchone()
            except Exception as e:
                return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)

        if not row:
            return Response({'error': 'Training type not found.'}, status=status.HTTP_404_NOT_FOUND)

        training_type = {
            'id_training_type': row[0],
            'name': row[1],
            'description': row[2],
            'hours': row[3],
        }
        return Response(training_type, status=status.HTTP_200_OK)
    
    
    @check_permission_decorator('create_training_type')
    def create(self, request):
        """
        Create a new training type.
        """
        serializer = self.serializer_class(data=request.data)

        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        data = serializer.validated_data

        with connection.cursor() as cursor:
            try:
                cursor.execute(
                    """
                    INSERT INTO training_types (name, description, hours)
                    VALUES (%s, %s, %s)
                    RETURNING id_training_type;
                    """,
                    [data['name'], data['description'], data.get('hours')]
                )
                new_id = cursor.fetchone()[0]
            except Exception as e:
                return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)

        return Response({'message': 'Training type created.', 'id_training_type': new_id}, status=status.HTTP_201_CREATED)

    
    @check_permission_decorator('update_training_type')
    def update(self, request, pk=None):
        """
        Update a training type by ID.
        """
        if not pk:
            return Response({'error': 'ID (pk) is required for updating a training type.'},
                            status=status.HTTP_400_BAD_REQUEST)

        serializer = self.serializer_class(data=request.data)

        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        data = serializer.validated_data

        with connection.cursor() as cursor:
            try:
                cursor.execute(
                    """
                    UPDATE training_types
                    SET name = %s, description = %s, hours = %s, updated_at = NOW()
                    WHERE id_training_type = %s;
                    """,
                    [data['name'], data['description'], data.get('hours'), pk]
                )
                if cursor.rowcount == 0:
                    return Response({'error': 'Training type not found.'}, status=status.HTTP_404_NOT_FOUND)
            except Exception as e:
                return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)

        return Response({'message': 'Training type updated successfully.'}, status=status.HTTP_200_OK)

    
    @check_permission_decorator('delete_training_type')
    def destroy(self, request, pk=None):
        """
        Delete a training type by ID.
        """
        if not pk:
            return Response({'error': 'ID (pk) is required for deleting a training type.'},
                            status=status.HTTP_400_BAD_REQUEST)

        with connection.cursor() as cursor:
            try:
                cursor.execute(
                    """
                    DELETE FROM training_types
                    WHERE id_training_type = %s;
                    """,
                    [pk]
                )
                if cursor.rowcount == 0:
                    return Response({'error': 'Training type not found.'}, status=status.HTTP_404_NOT_FOUND)
            except Exception as e:
                return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)

        return Response({'message': 'Training type deleted successfully.'}, status=status.HTTP_200_OK)
