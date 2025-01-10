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

class DeductionsViewSet(ViewSet):
    if not is_debug_mode():
        authentication_classes = [JWTAuthentication]
        permission_classes = [IsAuthenticated]

    """
    /api/deductions/?id_payment=<id_payment>
    """
    @check_permission_decorator('view_all_deductions')
    def list(self, request):
        id_payment = request.query_params.get('id_payment', None)
        id_employee = request.query_params.get('id_employee', None)

        query = """
            SELECT d.*, p.id_payment, ar.id_employee
            FROM deductions d
            INNER JOIN payments p ON d.id_payment = p.id_payment
            INNER JOIN absence_reason ar ON d.id_absence_reason = ar.id_absence_reason
        """
        if id_payment:
            query += " WHERE p.id_payment = %s"
            params = [id_payment]
        if id_employee:
            query += " WHERE ar.id_employee = %s ORDER BY d.deduction_date DESC"
            params = [id_employee]
        else:
            params = []

        with connection.cursor() as cursor:
            cursor.execute(query, params)
            columns = [col[0] for col in cursor.description]
            deductions = [dict(zip(columns, row)) for row in cursor.fetchall()]

        return Response(deductions, status=status.HTTP_200_OK)

    @check_permission_decorator('create_deduction')
    def create(self, request):
        data = request.data
        try:
            with connection.cursor() as cursor:
                cursor.execute("""
                    INSERT INTO deductions (id_payment, id_absence_reason, deduction_note, amount, deduction_date)
                    VALUES (%s, %s, %s, %s, %s)
                    RETURNING id_deduction
                """, [
                    data['id_payment'],
                    data['id_absence_reason'],
                    data.get('deduction_note', None),
                    data['amount'],
                    data['deduction_date']
                ])
                id_deduction = cursor.fetchone()[0]

            return Response({'id_deduction': id_deduction}, status=status.HTTP_201_CREATED)

        except Exception as e:
            return Response({'detail': str(e)}, status=status.HTTP_400_BAD_REQUEST)
    """
        - GET /api/deductions/<id_deduction>/
        - PUT /api/deductions/<id_deduction>/
        - DELETE /api/deductions/<id_deduction>/
    """
    @action(detail=False, methods=['get', 'put', 'delete'], url_path=r'(?P<id_deduction>[^/]+)')
    def handle(self, request, id_deduction):
        
        try:
            if request.method == 'GET':
                check_permission(request.user, 'view_deduction')

                query = """
                    SELECT * FROM deductions WHERE id_deduction = %s
                """
                with connection.cursor() as cursor:
                    cursor.execute(query, [id_deduction])
                    row = cursor.fetchone()
                    if row:
                        columns = [col[0] for col in cursor.description]
                        deduction = dict(zip(columns, row))
                        return Response(deduction, status=status.HTTP_200_OK)
                    else:
                        return Response({'detail': 'Deduction not found'}, status=status.HTTP_404_NOT_FOUND)

            elif request.method == 'PUT':
                check_permission(request.user, 'update_deduction')
                data = request.data

                query = """
                    UPDATE deductions
                    SET id_payment = %s, id_absence_reason = %s, deduction_note = %s,
                        amount = %s, deduction_date = %s, updated_at = CURRENT_TIMESTAMP
                    WHERE id_deduction = %s
                """
                with connection.cursor() as cursor:
                    cursor.execute(query, [
                        data['id_payment'],
                        data['id_absence_reason'],
                        data.get('deduction_note', None),
                        data['amount'],
                        data['deduction_date'],
                        id_deduction
                    ])

                return Response({'detail': 'Deduction updated successfully'}, status=status.HTTP_200_OK)

            elif request.method == 'DELETE':
                check_permission(request.user, 'delete_deduction')

                query = """
                    DELETE FROM deductions WHERE id_deduction = %s
                """
                with connection.cursor() as cursor:
                    cursor.execute(query, [id_deduction])
                    return Response({'detail': 'Deduction deleted successfully'}, status=status.HTTP_200_OK)

            return Response({'detail': f'Method {request.method} not allowed'}, status=status.HTTP_405_METHOD_NOT_ALLOWED)

        except Exception as e:
            return Response({'detail': str(e)}, status=status.HTTP_400_BAD_REQUEST)