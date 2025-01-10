from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import status
from django.db import connection
from rest_framework import serializers
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication
from api.utils.dotenv import is_debug_mode 
from api.utils.permissions import check_permission_decorator

class ContractTypeSerializer(serializers.Serializer):
    id_contract_type = serializers.UUIDField(read_only=True)
    contract_type_name = serializers.CharField(max_length=100, required=True)
    description = serializers.CharField(required=False, allow_blank=True)
    termination_notice_period = serializers.DecimalField(max_digits=10, decimal_places=2, required=False, allow_null=True)
    overtime_eligible = serializers.BooleanField(required=True)
    benefits_eligible = serializers.BooleanField(required=True)

class ContractTypeViewSet(ViewSet):
    """
    ViewSet for managing contract types.
    """
    serializer_class = ContractTypeSerializer
    
    if not is_debug_mode():
        authentication_classes = [JWTAuthentication]
        permission_classes = [IsAuthenticated]
        
        
    @check_permission_decorator('view_all_contract_types')
    def list(self, request):
        """
        List all contract types with optional filtering and pagination.
        """
        contract_type_name = request.GET.get('contract_type_name', None)
        limit = int(request.GET.get('limit', 10))
        offset = int(request.GET.get('offset', 0))

        with connection.cursor() as cursor:
            try:
                cursor.execute(
                    """
                    SELECT id_contract_type, contract_type_name, description, 
                           termination_notice_period, overtime_eligible, benefits_eligible
                    FROM contract_type
                    WHERE (%s IS NULL OR contract_type_name ILIKE %s)
                    LIMIT %s OFFSET %s;
                    """,
                    [contract_type_name, f"%{contract_type_name}%" if contract_type_name else None, limit, offset]
                )
                rows = cursor.fetchall()
            except Exception as e:
                return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)

        contract_types = [
            {
                'id_contract_type': row[0],
                'contract_type_name': row[1],
                'description': row[2],
                'termination_notice_period': row[3],
                'overtime_eligible': row[4],
                'benefits_eligible': row[5],
            }
            for row in rows
        ]
        return Response({'contract_types': contract_types}, status=status.HTTP_200_OK)

    
    @check_permission_decorator('view_contract_type')
    def retrieve(self, request, pk=None):
        """
        Retrieve a single contract type by ID.
        """
        with connection.cursor() as cursor:
            try:
                cursor.execute(
                    """
                    SELECT id_contract_type, contract_type_name, description, 
                           termination_notice_period, overtime_eligible, benefits_eligible
                    FROM contract_type
                    WHERE id_contract_type = %s;
                    """,
                    [pk]
                )
                row = cursor.fetchone()
            except Exception as e:
                return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)

        if not row:
            return Response({'error': 'Contract type not found.'}, status=status.HTTP_404_NOT_FOUND)

        contract_type = {
            'id_contract_type': row[0],
            'contract_type_name': row[1],
            'description': row[2],
            'termination_notice_period': row[3],
            'overtime_eligible': row[4],
            'benefits_eligible': row[5],
        }
        return Response(contract_type, status=status.HTTP_200_OK)

    
    @check_permission_decorator('create_contract_type')
    def create(self, request):
        """
        Create a new contract type.
        """
        serializer = self.serializer_class(data=request.data)

        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        data = serializer.validated_data

        with connection.cursor() as cursor:
            try:
                cursor.execute(
                    """
                    INSERT INTO contract_type (contract_type_name, description, 
                                               termination_notice_period, overtime_eligible, benefits_eligible)
                    VALUES (%s, %s, %s, %s, %s)
                    RETURNING id_contract_type;
                    """,
                    [data['contract_type_name'], data.get('description'), data.get('termination_notice_period'),
                     data['overtime_eligible'], data['benefits_eligible']]
                )
                new_id = cursor.fetchone()[0]
            except Exception as e:
                return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)

        return Response({'message': 'Contract type created.', 'id_contract_type': new_id}, status=status.HTTP_201_CREATED)

    
    @check_permission_decorator('update_contract_type')
    def update(self, request, pk=None):
        """
        Update a contract type by ID.
        """
        if not pk:
            return Response({'error': 'ID (pk) is required for updating a contract type.'},
                            status=status.HTTP_400_BAD_REQUEST)

        serializer = self.serializer_class(data=request.data)

        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        data = serializer.validated_data

        with connection.cursor() as cursor:
            try:
                cursor.execute(
                    """
                    UPDATE contract_type
                    SET contract_type_name = %s, description = %s, 
                        termination_notice_period = %s, overtime_eligible = %s, benefits_eligible = %s,
                        updated_at = NOW()
                    WHERE id_contract_type = %s;
                    """,
                    [data['contract_type_name'], data.get('description'), data.get('termination_notice_period'),
                     data['overtime_eligible'], data['benefits_eligible'], pk]
                )
                if cursor.rowcount == 0:
                    return Response({'error': 'Contract type not found.'}, status=status.HTTP_404_NOT_FOUND)
            except Exception as e:
                return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)

        return Response({'message': 'Contract type updated successfully.'}, status=status.HTTP_200_OK)

    
    @check_permission_decorator('delete_contract_type')
    def destroy(self, request, pk=None):
        """
        Delete a contract type by ID.
        """
        if not pk:
            return Response({'error': 'ID (pk) is required for deleting a contract type.'},
                            status=status.HTTP_400_BAD_REQUEST)

        with connection.cursor() as cursor:
            try:
                cursor.execute(
                    """
                    DELETE FROM contract_type
                    WHERE id_contract_type = %s;
                    """,
                    [pk]
                )
                if cursor.rowcount == 0:
                    return Response({'error': 'Contract type not found.'}, status=status.HTTP_404_NOT_FOUND)
            except Exception as e:
                return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)

        return Response({'message': 'Contract type deleted successfully.'}, status=status.HTTP_200_OK)
