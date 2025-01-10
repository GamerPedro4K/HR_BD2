from rest_framework.viewsets import ViewSet
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import status
from django.db import connection
from datetime import datetime

from api.utils.dotenv import is_debug_mode
from api.utils.permissions import check_permission_decorator, check_permission
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication

class BonusesViewSet(ViewSet):
    if not is_debug_mode():
        authentication_classes = [JWTAuthentication]
        permission_classes = [IsAuthenticated]

    """
    ViewSet para manipular a tabela 'bonuses'.
    """

    @check_permission_decorator('view_all_bonuses')
    def list(self, request):
        """
        Lista todos os bônus com suporte a filtros.
        """
        payment_id = request.query_params.get('payment_id', None)

        query = "SELECT * FROM bonuses"
        params = []

        if payment_id:
            query += " WHERE id_payment = %s"
            params.append(payment_id)

        with connection.cursor() as cursor:
            cursor.execute(query, params)
            columns = [col[0] for col in cursor.description]
            bonuses = [dict(zip(columns, row)) for row in cursor.fetchall()]

        return Response(bonuses, status=status.HTTP_200_OK)

    @check_permission_decorator('create_bonus')
    def create(self, request):
        """
        Cria um novo registro de bônus.
        """
        data = request.data
        try:
            with connection.cursor() as cursor:
                cursor.execute(
                    """
                    INSERT INTO bonuses (id_payment, bonus_note, amount, bonus_date)
                    VALUES (%s, %s, %s, %s)
                    RETURNING id_bonus
                    """,
                    [
                        data['id_payment'],
                        data['bonus_note'],
                        data['amount'],
                        data['bonus_date']
                    ]
                )
                id_bonus = cursor.fetchone()[0]

            return Response({'id_bonus': id_bonus}, status=status.HTTP_201_CREATED)

        except Exception as e:
            return Response({'detail': str(e)}, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=False, methods=['get', 'put', 'delete'], url_path=r'(?P<id_bonus>[^/]+)')
    def handle(self, request, id_bonus):
        """
        Lida com operações GET, PUT e DELETE em um único endpoint para a tabela 'bonuses'.
        """
        try:
            if request.method == 'GET':
                check_permission(request.user, 'view_bonus')

                query = "SELECT * FROM bonuses WHERE id_bonus = %s"
                with connection.cursor() as cursor:
                    cursor.execute(query, [id_bonus])
                    row = cursor.fetchone()
                    if row:
                        columns = [col[0] for col in cursor.description]
                        bonus = dict(zip(columns, row))
                        return Response(bonus, status=status.HTTP_200_OK)
                    else:
                        return Response({'detail': 'Bonus not found'}, status=status.HTTP_404_NOT_FOUND)

            elif request.method == 'PUT':
                check_permission(request.user, 'update_bonus')
                data = request.data

                query = """
                    UPDATE bonuses
                    SET id_payment = %s, bonus_note = %s, amount = %s, bonus_date = %s, updated_at = CURRENT_TIMESTAMP
                    WHERE id_bonus = %s
                    """
                with connection.cursor() as cursor:
                    cursor.execute(query, [
                        data['id_payment'],
                        data['bonus_note'],
                        data['amount'],
                        data['bonus_date'],
                        id_bonus
                    ])

                return Response({'detail': 'Bonus updated successfully'}, status=status.HTTP_200_OK)

            elif request.method == 'DELETE':
                check_permission(request.user, 'delete_bonus')

                query = "DELETE FROM bonuses WHERE id_bonus = %s"
                with connection.cursor() as cursor:
                    cursor.execute(query, [id_bonus])
                    return Response({'detail': 'Bonus deleted successfully'}, status=status.HTTP_200_OK)

            return Response({'detail': f'Method {request.method} not allowed'}, status=status.HTTP_405_METHOD_NOT_ALLOWED)

        except Exception as e:
            return Response({'detail': str(e)}, status=status.HTTP_400_BAD_REQUEST)
