from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import status
from django.db import connection
from rest_framework import serializers
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication
from api.utils.dotenv import is_debug_mode 
from api.utils.permissions import check_permission_decorator

class TypeBenefitSerializer(serializers.Serializer):
    id_type_benefit = serializers.UUIDField(read_only=True)
    name = serializers.CharField(max_length=100, required=True)
    description = serializers.CharField(required=True)


class TypeBenefitViewSet(ViewSet):
    """
    ViewSet for managing type benefits.
    """
    serializer_class = TypeBenefitSerializer
    
    if not is_debug_mode():
        authentication_classes = [JWTAuthentication]
        permission_classes = [IsAuthenticated]
        

    @check_permission_decorator('view_all_type_benefits')
    def list(self, request):
        """
        List all type benefits with optional filtering and pagination.
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
                    FROM get_all_type_benefits(
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

                type_benefits = []
                total_count = rows[0][-1] if rows else 0  # Last field is total_count

                for row in rows:
                    type_benefits.append({
                        'id_type_benefit': row[0],
                        'name': row[1],
                        'description': row[2]
                    })

                return Response({
                    'type_benefits': type_benefits,
                    'total_count': total_count
                }, status=status.HTTP_200_OK)

            except Exception as e:
                return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)
    
    
    @check_permission_decorator('view_type_benefit')
    def retrieve(self, request, pk=None):
        """
        Retrieve a single type benefit by ID.
        """
        with connection.cursor() as cursor:
            try:
                cursor.execute(
                    """
                    SELECT id_type_benefit, name, description
                    FROM type_benefit
                    WHERE id_type_benefit = %s;
                    """,
                    [pk]
                )
                row = cursor.fetchone()
            except Exception as e:
                return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)

        if not row:
            return Response({'error': 'Type benefit not found.'}, status=status.HTTP_404_NOT_FOUND)

        type_benefit = {
            'id_type_benefit': row[0],
            'name': row[1],
            'description': row[2],
        }
        return Response(type_benefit, status=status.HTTP_200_OK)

    
    @check_permission_decorator('create_type_benefit')
    def create(self, request):
        """
        Create a new type benefit.
        """
        serializer = self.serializer_class(data=request.data)

        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        data = serializer.validated_data

        with connection.cursor() as cursor:
            try:
                cursor.execute(
                    """
                    INSERT INTO type_benefit (name, description)
                    VALUES (%s, %s)
                    RETURNING id_type_benefit;
                    """,
                    [data['name'], data['description']]
                )
                new_id = cursor.fetchone()[0]
            except Exception as e:
                return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)

        return Response({'message': 'Type benefit created.', 'id_type_benefit': new_id}, status=status.HTTP_201_CREATED)

    
    @check_permission_decorator('update_type_benefit')
    def update(self, request, pk=None):
        """
        Update a type benefit by ID.
        """
        if not pk:
            return Response({'error': 'ID (pk) is required for updating a type benefit.'},
                            status=status.HTTP_400_BAD_REQUEST)

        serializer = self.serializer_class(data=request.data)

        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        data = serializer.validated_data

        with connection.cursor() as cursor:
            try:
                cursor.execute(
                    """
                    UPDATE type_benefit
                    SET name = %s, description = %s, updated_at = NOW()
                    WHERE id_type_benefit = %s;
                    """,
                    [data['name'], data['description'], pk]
                )
                if cursor.rowcount == 0:
                    return Response({'error': 'Type benefit not found.'}, status=status.HTTP_404_NOT_FOUND)
            except Exception as e:
                return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)

        return Response({'message': 'Type benefit updated successfully.'}, status=status.HTTP_200_OK)

    
    @check_permission_decorator('delete_type_benefit')
    def destroy(self, request, pk=None):
        """
        Delete a type benefit by ID.
        """
        if not pk:
            return Response({'error': 'ID (pk) is required for deleting a type benefit.'},
                            status=status.HTTP_400_BAD_REQUEST)

        with connection.cursor() as cursor:
            try:
                cursor.execute(
                    """
                    DELETE FROM type_benefit
                    WHERE id_type_benefit = %s;
                    """,
                    [pk]
                )
                if cursor.rowcount == 0:
                    return Response({'error': 'Type benefit not found.'}, status=status.HTTP_404_NOT_FOUND)
            except Exception as e:
                return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)

        return Response({'message': 'Type benefit deleted successfully.'}, status=status.HTTP_200_OK)
