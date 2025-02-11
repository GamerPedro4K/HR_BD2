from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import status
from django.db import connection
from rest_framework import serializers
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication
from api.utils.dotenv import is_debug_mode 
from api.utils.permissions import check_permission_decorator

class PaymentMethodSerializer(serializers.Serializer):
    id_payment_method = serializers.UUIDField(read_only=True)
    name = serializers.CharField(max_length=50, required=True)
    description = serializers.CharField(required=True)
    icon = serializers.CharField(max_length=100, required=True)
    hex_color = serializers.CharField(max_length=7, required=True)
    
class PaymentMethodViewSet(ViewSet):
    """
    ViewSet for managing payment methods.
    """
    serializer_class = PaymentMethodSerializer
    
    if not is_debug_mode():
        authentication_classes = [JWTAuthentication]
        permission_classes = [IsAuthenticated]
        

    @check_permission_decorator('view_all_payment_methods')
    def list(self, request):
        """
        List all payment methods with optional filtering and pagination.
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
                    FROM get_all_payment_methods(
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

                payment_methods = []
                total_count = rows[0][-1] if rows else 0  # Last field is total_count

                for row in rows:
                    payment_methods.append({
                        'id_payment_method': row[0],
                        'name': row[1],
                        'description': row[2],
                        'icon': row[3],
                        'hex_color': row[4]
                    })

                return Response({
                    'payment_methods': payment_methods,
                    'total_count': total_count
                }, status=status.HTTP_200_OK)

            except Exception as e:
                return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)

        
    @check_permission_decorator('view_payment_method')
    def retrieve(self, request, pk=None):
        """
        Retrieve a single payment method by ID.
        """
        with connection.cursor() as cursor:
            try:
                cursor.execute(
                    """
                    SELECT id_payment_method, name, description, icon, hex_color
                    FROM payment_methods
                    WHERE id_payment_method = %s;
                    """,
                    [pk]
                )
                row = cursor.fetchone()
            except Exception as e:
                return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)

        if not row:
            return Response({'error': 'Payment method not found.'}, status=status.HTTP_404_NOT_FOUND)

        payment_method = {
            'id_payment_method': row[0],
            'name': row[1],
            'description': row[2],
            'icon': row[3],
            'hex_color': row[4],
        }
        return Response(payment_method, status=status.HTTP_200_OK)

    
    @check_permission_decorator('create_payment_method')
    def create(self, request):
        """
        Create a new payment method.
        """
        serializer = self.serializer_class(data=request.data)

        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        data = serializer.validated_data

        with connection.cursor() as cursor:
            try:
                cursor.execute(
                    """
                    INSERT INTO payment_methods (name, description, icon, hex_color)
                    VALUES (%s, %s, %s, %s)
                    RETURNING id_payment_method;
                    """,
                    [data['name'], data['description'], data['icon'], data['hex_color']]
                )
                new_id = cursor.fetchone()[0]
            except Exception as e:
                return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)

        return Response({'message': 'Payment method created.', 'id_payment_method': new_id}, status=status.HTTP_201_CREATED)


    @check_permission_decorator('update_payment_method')
    def update(self, request, pk=None):
        """
        Update a payment method by ID.
        """
        if not pk:
            return Response({'error': 'ID (pk) is required for updating a payment method.'},
                            status=status.HTTP_400_BAD_REQUEST)

        serializer = self.serializer_class(data=request.data)

        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        data = serializer.validated_data

        with connection.cursor() as cursor:
            try:
                cursor.execute(
                    """
                    UPDATE payment_methods
                    SET name = %s, description = %s, icon = %s, hex_color = %s, updated_at = NOW()
                    WHERE id_payment_method = %s;
                    """,
                    [data['name'], data['description'], data['icon'], data['hex_color'], pk]
                )
                if cursor.rowcount == 0:
                    return Response({'error': 'Payment method not found.'}, status=status.HTTP_404_NOT_FOUND)
            except Exception as e:
                return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)

        return Response({'message': 'Payment method updated successfully.'}, status=status.HTTP_200_OK)

    
    @check_permission_decorator('delete_payment_method')
    def destroy(self, request, pk=None):
        """
        Delete a payment method by ID.
        """
        if not pk:
            return Response({'error': 'ID (pk) is required for deleting a payment method.'},
                            status=status.HTTP_400_BAD_REQUEST)

        with connection.cursor() as cursor:
            try:
                cursor.execute(
                    """
                    DELETE FROM payment_methods
                    WHERE id_payment_method = %s;
                    """,
                    [pk]
                )
                if cursor.rowcount == 0:
                    return Response({'error': 'Payment method not found.'}, status=status.HTTP_404_NOT_FOUND)
            except Exception as e:
                return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)

        return Response({'message': 'Payment method deleted successfully.'}, status=status.HTTP_200_OK)
