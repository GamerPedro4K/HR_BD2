from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import status
from django.db import connection
from rest_framework import serializers
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication
from api.utils.dotenv import is_debug_mode
from api.utils.permissions import check_permission_decorator

class ContractStateContractSerializer(serializers.Serializer):
    id_contract_state_contract = serializers.UUIDField(read_only=True)
    id_contract_state = serializers.UUIDField(required=True)
    id_contract = serializers.UUIDField(required=True)
    created_at = serializers.DateTimeField(read_only=True, allow_null=True)
    updated_at = serializers.DateTimeField(read_only=True, allow_null=True)
    deleted_at = serializers.DateTimeField(read_only=True, allow_null=True, required=False)

class ContractStateContractViewSet(ViewSet):
    """
    ViewSet for managing contract state contracts.
    """
    serializer_class = ContractStateContractSerializer
    
    if not is_debug_mode():
        authentication_classes = [JWTAuthentication]
        permission_classes = [IsAuthenticated]

    @check_permission_decorator('view_all_contract_state_contracts')
    def list(self, request):
        """
        List all contract state contracts with optional filtering and pagination.
        """
        limit = int(request.GET.get('limit', 10))
        offset = int(request.GET.get('offset', 0))
        count = 0

        with connection.cursor() as cursor:
            try:
                cursor.execute(
                    """
                    SELECT 
                        contract_state_contract.id_contract_state_contract, 
                        contract_state_contract.id_contract_state, 
                        contract_state_contract.id_contract, 
                        contract_state_contract.created_at, 
                        contract_state_contract.updated_at, 
                        contract_state.icon, 
                        contract_state.hex_color, 
                        contract_state.state, 
                        contract_state.description
                    FROM contract_state_contract
                    INNER JOIN contract_state ON contract_state_contract.id_contract_state = contract_state.id_contract_state
                    WHERE contract_state_contract.deleted_at is null
                    LIMIT %s OFFSET %s;
                    """,
                    [limit, offset]
                )
                rows = cursor.fetchall()
                cursor.execute(
                    """
                    SELECT COUNT(*) 
                    FROM contract_state_contract
                    WHERE deleted_at is null;
                    """
                )
                count = cursor.fetchone()[0]
            except Exception as e:
                return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)

        contract_state_contracts = [
            {
                'contract_state': {
                    'id_contract_state_contract': row[0],
                    'id_contract': row[2],
                    'created_at': row[3],
                    'updated_at': row[4]
                },
                'state': {
                    'id_contract_state': row[1],
                    'icon': row[5],
                    'hex_color': row[6],
                    'state': row[7],
                    'description': row[8],
                },
            }
            for row in rows
        ]

        return Response({'data': contract_state_contracts, 'count': count}, status=status.HTTP_200_OK)

    @check_permission_decorator('view_contract_state_contract')
    def retrieve(self, request, pk=None):
        """
        List all contract state contracts for a specific employee.
        """
        limit = int(request.GET.get('limit', 10))
        offset = int(request.GET.get('offset', 0))
        count = 0

        with connection.cursor() as cursor:
            try:
                cursor.execute(
                    """
                    SELECT 
                        contract_state_contract.id_contract_state_contract, 
                        contract_state_contract.id_contract_state, 
                        contract_state_contract.id_contract, 
                        contract_state_contract.created_at, 
                        contract_state_contract.updated_at, 
                        contract_state.icon, 
                        contract_state.hex_color, 
                        contract_state.state, 
                        contract_state.description
                    FROM contract_state_contract
                    INNER JOIN contract_state ON contract_state_contract.id_contract_state = contract_state.id_contract_state
                    INNER JOIN contract ON contract_state_contract.id_contract = contract.id_contract
                    WHERE contract.id_employee = %s
                    AND contract_state_contract.deleted_at IS NULL
                    ORDER BY contract_state_contract.created_at DESC
                    LIMIT %s OFFSET %s;
                    """,
                    [pk, limit, offset]
                )
                rows = cursor.fetchall()
                
                cursor.execute(
                    """
                    SELECT COUNT(*) 
                    FROM contract_state_contract
                    INNER JOIN contract ON contract_state_contract.id_contract = contract.id_contract
                    WHERE contract.id_employee = %s
                    AND contract_state_contract.deleted_at IS NULL;
                    """,
                    [pk]
                )
                count = cursor.fetchone()[0]

            except Exception as e:
                return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)

        contract_state_contracts = [
            {
                'contract_state': {
                    'id_contract_state_contract': row[0],
                    'id_contract': row[2],
                    'created_at': row[3],
                    'updated_at': row[4]
                },
                'state': {
                    'id_contract_state': row[1],
                    'icon': row[5],
                    'hex_color': row[6],
                    'state': row[7],
                    'description': row[8],
                },
            }
            for row in rows
        ]

        return Response({'data': contract_state_contracts, 'count': count}, status=status.HTTP_200_OK)


    @check_permission_decorator('create_contract_state_contract')
    def create(self, request):
        """
        Create a new contract state contract.
        """
        serializer = self.serializer_class(data=request.data)

        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        data = serializer.validated_data

        with connection.cursor() as cursor:
            try:
                cursor.execute(
                    """
                    INSERT INTO contract_state_contract (id_contract_state, id_contract)
                    VALUES (%s, %s)
                    RETURNING id_contract_state_contract;
                    """,
                    [data['id_contract_state'], data['id_contract']]
                )
                new_id = cursor.fetchone()[0]
            except Exception as e:
                return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)

        return Response({'message': 'Contract state contract created.', 'id_contract_state_contract': new_id}, status=status.HTTP_201_CREATED)

    @check_permission_decorator('update_contract_state_contract')
    def update(self, request, pk=None):
        """
        Update a contract state contract by ID.
        """
        if not pk:
            return Response({'error': 'ID (pk) is required for updating a contract state contract.'},
                            status=status.HTTP_400_BAD_REQUEST)

        serializer = self.serializer_class(data=request.data)

        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        data = serializer.validated_data

        with connection.cursor() as cursor:
            try:
                cursor.execute(
                    """
                    UPDATE contract_state_contract
                    SET id_contract_state = %s, id_contract = %s, updated_at = NOW()
                    WHERE id_contract_state_contract = %s;
                    """,
                    [data['id_contract_state'], data['id_contract'], pk]
                )
                if cursor.rowcount == 0:
                    return Response({'error': 'Contract state contract not found.'}, status=status.HTTP_404_NOT_FOUND)
            except Exception as e:
                return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)

        return Response({'message': 'Contract state contract updated successfully.'}, status=status.HTTP_200_OK)

    @check_permission_decorator('delete_contract_state_contract')
    def destroy(self, request, pk=None):
        """
        Soft delete a contract state contract by ID.
        """
        if not pk:
            return Response({'error': 'ID (pk) is required for deleting a contract state contract.'},
                            status=status.HTTP_400_BAD_REQUEST)

        with connection.cursor() as cursor:
            try:
                cursor.execute(
                    """
                    UPDATE contract_state_contract
                    SET deleted_at = NOW()
                    WHERE id_contract_state_contract = %s;
                    """,
                    [pk]
                )
                if cursor.rowcount == 0:
                    return Response({'error': 'Contract state contract not found.'}, status=status.HTTP_404_NOT_FOUND)
            except Exception as e:
                return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)

        return Response({'message': 'Contract state contract deleted successfully.'}, status=status.HTTP_200_OK)
