from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import status
from django.db import connection
from rest_framework import serializers
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication
from api.utils.dotenv import is_debug_mode 
from api.utils.permissions import check_permission_decorator

class ContractStateSerializer(serializers.Serializer):
    id_contract_state = serializers.UUIDField(read_only=True)
    icon = serializers.CharField(max_length=100, required=True)
    hex_color = serializers.CharField(max_length=7, required=True)
    state = serializers.CharField(max_length=100, required=True)
    description = serializers.CharField(required=False, allow_blank=True)

class ContractStateViewSet(ViewSet):
    """
    ViewSet for managing contract states.
    """
    serializer_class = ContractStateSerializer
    
    if not is_debug_mode():
        authentication_classes = [JWTAuthentication]
        permission_classes = [IsAuthenticated]
        
        
    @check_permission_decorator('view_all_certificate_types')
    def list(self, request):
        """
        List all contract states with optional filtering and pagination.
        """
        state = request.GET.get('state', None)
        limit = int(request.GET.get('limit', 10))
        offset = int(request.GET.get('offset', 0))

        with connection.cursor() as cursor:
            try:
                cursor.execute(
                    """
                    SELECT id_contract_state, icon, hex_color, state, description
                    FROM contract_state
                    WHERE (%s IS NULL OR state ILIKE %s)
                    LIMIT %s OFFSET %s;
                    """,
                    [state, f"%{state}%" if state else None, limit, offset]
                )
                rows = cursor.fetchall()
            except Exception as e:
                return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)

        contract_states = [
            {
                'id_contract_state': row[0],
                'icon': row[1],
                'hex_color': row[2],
                'state': row[3],
                'description': row[4],
            }
            for row in rows
        ]
        return Response({'contract_states': contract_states}, status=status.HTTP_200_OK)


    @check_permission_decorator('view_all_certificate_types')
    def retrieve(self, request, pk=None):
        """
        Retrieve a single contract state by ID.
        """
        with connection.cursor() as cursor:
            try:
                cursor.execute(
                    """
                    SELECT id_contract_state, icon, hex_color, state, description
                    FROM contract_state
                    WHERE id_contract_state = %s;
                    """,
                    [pk]
                )
                row = cursor.fetchone()
            except Exception as e:
                return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)

        if not row:
            return Response({'error': 'Contract state not found.'}, status=status.HTTP_404_NOT_FOUND)

        contract_state = {
            'id_contract_state': row[0],
            'icon': row[1],
            'hex_color': row[2],
            'state': row[3],
            'description': row[4],
        }
        return Response(contract_state, status=status.HTTP_200_OK)


    @check_permission_decorator('view_all_certificate_types')
    def create(self, request):
        """
        Create a new contract state.
        """
        serializer = self.serializer_class(data=request.data)

        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        data = serializer.validated_data

        with connection.cursor() as cursor:
            try:
                cursor.execute(
                    """
                    INSERT INTO contract_state (icon, hex_color, state, description)
                    VALUES (%s, %s, %s, %s)
                    RETURNING id_contract_state;
                    """,
                    [data['icon'], data['hex_color'], data['state'], data.get('description')]
                )
                new_id = cursor.fetchone()[0]
            except Exception as e:
                return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)

        return Response({'message': 'Contract state created.', 'id_contract_state': new_id}, status=status.HTTP_201_CREATED)


    @check_permission_decorator('view_all_certificate_types')
    def update(self, request, pk=None):
        """
        Update a contract state by ID.
        """
        if not pk:
            return Response({'error': 'ID (pk) is required for updating a contract state.'},
                            status=status.HTTP_400_BAD_REQUEST)

        serializer = self.serializer_class(data=request.data)

        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        data = serializer.validated_data

        with connection.cursor() as cursor:
            try:
                cursor.execute(
                    """
                    UPDATE contract_state
                    SET icon = %s, hex_color = %s, state = %s, description = %s, updated_at = NOW()
                    WHERE id_contract_state = %s;
                    """,
                    [data['icon'], data['hex_color'], data['state'], data.get('description'), pk]
                )
                if cursor.rowcount == 0:
                    return Response({'error': 'Contract state not found.'}, status=status.HTTP_404_NOT_FOUND)
            except Exception as e:
                return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)

        return Response({'message': 'Contract state updated successfully.'}, status=status.HTTP_200_OK)
    
    
    @check_permission_decorator('view_all_certificate_types')
    def destroy(self, request, pk=None):
        """
        Delete a contract state by ID.
        """
        if not pk:
            return Response({'error': 'ID (pk) is required for deleting a contract state.'},
                            status=status.HTTP_400_BAD_REQUEST)

        with connection.cursor() as cursor:
            try:
                cursor.execute(
                    """
                    DELETE FROM contract_state
                    WHERE id_contract_state = %s;
                    """,
                    [pk]
                )
                if cursor.rowcount == 0:
                    return Response({'error': 'Contract state not found.'}, status=status.HTTP_404_NOT_FOUND)
            except Exception as e:
                return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)

        return Response({'message': 'Contract state deleted successfully.'}, status=status.HTTP_200_OK)
