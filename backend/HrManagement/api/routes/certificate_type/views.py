from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import status
from django.db import connection
from rest_framework import serializers
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication
from api.utils.dotenv import is_debug_mode 
from api.utils.permissions import check_permission_decorator


class CertificateTypeSerializer(serializers.Serializer):
    name = serializers.CharField(max_length=255, required=True)
    description = serializers.CharField(required=True)
    icon = serializers.CharField(max_length=255, required=True)
    hex_color = serializers.CharField(max_length=7, required=True)


class CertificateTypeViewSet(ViewSet):
    """
    ViewSet to handle certificate_types operations with serializer integration.
    """

    serializer_class = CertificateTypeSerializer  # Attach the serializer here
    
    if not is_debug_mode():
        authentication_classes = [JWTAuthentication]
        permission_classes = [IsAuthenticated]
        
    @check_permission_decorator('view_all_certificate_types')
    def list(self, request):
        """
        List all certificate types with optional filtering and pagination.
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
                    FROM get_all_certificate_types(
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

                certificate_types = []
                total_count = rows[0][-1] if rows else 0  # Last field is total_count

                for row in rows:
                    certificate_types.append({
                        'id_certificate_type': row[0],
                        'name': row[1],
                        'description': row[2],
                        'icon': row[3],
                        'hex_color': row[4]
                    })

                return Response({
                    'certificate_types': certificate_types,
                    'total_count': total_count
                }, status=status.HTTP_200_OK)

            except Exception as e:
                return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)

    @check_permission_decorator('view_certificate_type')
    def retrieve(self, request, pk=None):
        """
        Retrieve a specific certificate type by ID.
        """
        with connection.cursor() as cursor:
            try:
                cursor.execute(
                    """
                    SELECT id_certificate_type, name, description, icon, hex_color
                    FROM certificate_types
                    WHERE id_certificate_type = %s;
                    """,
                    [pk]
                )
                row = cursor.fetchone()
            except Exception as e:
                return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)

        if row is None:
            return Response({'error': 'Certificate type not found.'}, status=status.HTTP_404_NOT_FOUND)

        certificate = {
            'id_certificate_type': row[0],
            'name': row[1],
            'description': row[2],
            'icon': row[3],
            'hex_color': row[4],
        }
        return Response(certificate, status=status.HTTP_200_OK)

    @check_permission_decorator('create_certificate_type')
    def create(self, request):
        """
        Create a new certificate type.
        """
        serializer = self.serializer_class(data=request.data)  # Use serializer_class here

        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        data = serializer.validated_data
        name = data['name']
        description = data['description']
        icon = data['icon']
        hex_color = data['hex_color']

        with connection.cursor() as cursor:
            try:
                cursor.execute(
                    """
                    INSERT INTO certificate_types (name, description, icon, hex_color)
                    VALUES (%s, %s, %s, %s)
                    RETURNING id_certificate_type;
                    """,
                    [name, description, icon, hex_color]
                )
                new_id = cursor.fetchone()[0]
            except Exception as e:
                return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)

        return Response({'message': 'Certificate type created.', 'id_certificate_type': new_id}, status=status.HTTP_201_CREATED)

    @check_permission_decorator('update_certificate_type')
    def update(self, request, pk=None):
        """
        Update a certificate type by ID.
        """
        if not pk:
            return Response({'error': 'ID (pk) is required for updating a certificate type.'},
                            status=status.HTTP_400_BAD_REQUEST)

        serializer = self.serializer_class(data=request.data)  # Use serializer_class here

        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        data = serializer.validated_data
        name = data['name']
        description = data['description']
        icon = data['icon']
        hex_color = data['hex_color']

        with connection.cursor() as cursor:
            try:
                cursor.execute(
                    """
                    UPDATE certificate_types
                    SET name = %s, description = %s, icon = %s, hex_color = %s, updated_at = NOW()
                    WHERE id_certificate_type = %s;
                    """,
                    [name, description, icon, hex_color, pk]
                )
                if cursor.rowcount == 0:
                    return Response({'error': 'Certificate type not found.'}, status=status.HTTP_404_NOT_FOUND)
            except Exception as e:
                return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)

        return Response({'message': 'Certificate type updated successfully.'}, status=status.HTTP_200_OK)

    @check_permission_decorator('delete_certificate_type')
    def destroy(self, request, pk=None):
        """
        Delete a certificate type by ID.
        """
        if not pk:
            return Response({'error': 'ID (pk) is required for deleting a certificate type.'},
                            status=status.HTTP_400_BAD_REQUEST)

        with connection.cursor() as cursor:
            try:
                cursor.execute(
                    """
                    DELETE FROM certificate_types
                    WHERE id_certificate_type = %s;
                    """,
                    [pk]
                )
                if cursor.rowcount == 0:
                    return Response({'error': 'Certificate type not found.'}, status=status.HTTP_404_NOT_FOUND)
            except Exception as e:
                return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)

        return Response({'message': 'Certificate type deleted successfully.'}, status=status.HTTP_200_OK)
