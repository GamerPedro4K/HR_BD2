from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import status
from django.db import connection
from rest_framework import serializers
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication
from api.utils.dotenv import is_debug_mode 
from api.utils.permissions import check_permission_decorator

class ContractLeaveTypeSerializer(serializers.Serializer):
    id_leave_type = serializers.UUIDField(read_only=True)
    leave_type = serializers.CharField(max_length=100, required=True)
    description = serializers.CharField(required=False, allow_blank=True)
    is_paid = serializers.BooleanField(required=True)

class ContractLeaveTypeViewSet(ViewSet):
    """
    ViewSet for managing contract leave types.
    """
    serializer_class = ContractLeaveTypeSerializer
    
    if not is_debug_mode():
        authentication_classes = [JWTAuthentication]
        permission_classes = [IsAuthenticated]
        
    @check_permission_decorator('view_all_contract_leave_types')
    def list(self, request):
        """
        List all contract leave types with optional filtering and pagination.
        """
        leave_type = request.GET.get('leave_type', None)
        limit = int(request.GET.get('limit', 10))
        offset = int(request.GET.get('offset', 0))

        with connection.cursor() as cursor:
            try:
                cursor.execute(
                    """
                    SELECT id_leave_type, leave_type, description, is_paid
                    FROM contract_leave_type
                    WHERE (%s IS NULL OR leave_type ILIKE %s)
                    LIMIT %s OFFSET %s;
                    """,
                    [leave_type, f"%{leave_type}%" if leave_type else None, limit, offset]
                )
                rows = cursor.fetchall()
            except Exception as e:
                return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)

        contract_leave_types = [
            {
                'id_leave_type': row[0],
                'leave_type': row[1],
                'description': row[2],
                'is_paid': row[3],
            }
            for row in rows
        ]
        return Response({'contract_leave_types': contract_leave_types}, status=status.HTTP_200_OK)

    @check_permission_decorator('view_contract_leave_type')
    def retrieve(self, request, pk=None):
        """
        Retrieve a single contract leave type by ID.
        """
        with connection.cursor() as cursor:
            try:
                cursor.execute(
                    """
                    SELECT id_leave_type, leave_type, description, is_paid
                    FROM contract_leave_type
                    WHERE id_leave_type = %s;
                    """,
                    [pk]
                )
                row = cursor.fetchone()
            except Exception as e:
                return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)

        if not row:
            return Response({'error': 'Contract leave type not found.'}, status=status.HTTP_404_NOT_FOUND)

        contract_leave_type = {
            'id_leave_type': row[0],
            'leave_type': row[1],
            'description': row[2],
            'is_paid': row[3],
        }
        return Response(contract_leave_type, status=status.HTTP_200_OK)


    @check_permission_decorator('create_contract_leave_type')
    def create(self, request):
        """
        Create a new contract leave type.
        """
        serializer = self.serializer_class(data=request.data)

        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        data = serializer.validated_data

        with connection.cursor() as cursor:
            try:
                cursor.execute(
                    """
                    INSERT INTO contract_leave_type (leave_type, description, is_paid)
                    VALUES (%s, %s, %s)
                    RETURNING id_leave_type;
                    """,
                    [data['leave_type'], data.get('description'), data['is_paid']]
                )
                new_id = cursor.fetchone()[0]
            except Exception as e:
                return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)

        return Response({'message': 'Contract leave type created.', 'id_leave_type': new_id}, status=status.HTTP_201_CREATED)


    @check_permission_decorator('update_contract_leave_type')
    def update(self, request, pk=None):
        """
        Update a contract leave type by ID.
        """
        if not pk:
            return Response({'error': 'ID (pk) is required for updating a contract leave type.'},
                            status=status.HTTP_400_BAD_REQUEST)

        serializer = self.serializer_class(data=request.data)

        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        data = serializer.validated_data

        with connection.cursor() as cursor:
            try:
                cursor.execute(
                    """
                    UPDATE contract_leave_type
                    SET leave_type = %s, description = %s, is_paid = %s, updated_at = NOW()
                    WHERE id_leave_type = %s;
                    """,
                    [data['leave_type'], data.get('description'), data['is_paid'], pk]
                )
                if cursor.rowcount == 0:
                    return Response({'error': 'Contract leave type not found.'}, status=status.HTTP_404_NOT_FOUND)
            except Exception as e:
                return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)

        return Response({'message': 'Contract leave type updated successfully.'}, status=status.HTTP_200_OK)


    @check_permission_decorator('delete_contract_leave_type')
    def destroy(self, request, pk=None):
        """
        Delete a contract leave type by ID.
        """
        if not pk:
            return Response({'error': 'ID (pk) is required for deleting a contract leave type.'},
                            status=status.HTTP_400_BAD_REQUEST)

        with connection.cursor() as cursor:
            try:
                cursor.execute(
                    """
                    DELETE FROM contract_leave_type
                    WHERE id_leave_type = %s;
                    """,
                    [pk]
                )
                if cursor.rowcount == 0:
                    return Response({'error': 'Contract leave type not found.'}, status=status.HTTP_404_NOT_FOUND)
            except Exception as e:
                return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)

        return Response({'message': 'Contract leave type deleted successfully.'}, status=status.HTTP_200_OK)
