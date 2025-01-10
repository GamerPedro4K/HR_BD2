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

class PaymentsViewSet(ViewSet):
    if not is_debug_mode():
        authentication_classes = [JWTAuthentication]
        permission_classes = [IsAuthenticated]

    @check_permission_decorator('view_all_payments')
    def list(self, request):
        """
        URL: /api/payments/?id_employee=<id_employee>
        """
        id_employee = request.query_params.get('id_employee', None)

        query = """
            SELECT p.*, e.id_employee AS employee_id, pm.name AS payment_method_name
            FROM payments p
            INNER JOIN employees e ON p.id_employee = e.id_employee
            INNER JOIN payment_methods pm ON p.id_payment_method = pm.id_payment_method
        """
        if id_employee:
            query += " WHERE p.id_employee = %s"
            params = [id_employee]
        else:
            params = []

        with connection.cursor() as cursor:
            cursor.execute(query, params)
            columns = [col[0] for col in cursor.description]
            payments = [dict(zip(columns, row)) for row in cursor.fetchall()]

        return Response(payments, status=status.HTTP_200_OK)

    @check_permission_decorator('create_payment')
    def create(self, request):
        data = request.data
        try:
            with connection.cursor() as cursor:
                cursor.execute("""
                    INSERT INTO payments (id_employee, id_employee_supervisor, id_payment_method, amount, payment_date, extra_amount, deduction_amount, bonus_amount, payment_note, src)
                    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                    RETURNING id_payment
                """, [
                    data['id_employee'],
                    data['id_employee_supervisor'],
                    data['id_payment_method'],
                    data['amount'],
                    data['payment_date'],
                    data.get('extra_amount'),
                    data.get('deduction_amount'),
                    data.get('bonus_amount'),
                    data.get('payment_note'),
                    data.get('src')
                ])
                id_payment = cursor.fetchone()[0]

            return Response({'id_payment': id_payment}, status=status.HTTP_201_CREATED)

        except Exception as e:
            return Response({'detail': str(e)}, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=False, methods=['get', 'put', 'delete'], url_path=r'(?P<id_payment>[^/]+)')
    def handle(self, request, id_payment):
        """
        - GET /api/payments/<id_payment>/
        - PUT /api/payments/<id_payment>/
        - DELETE /api/payments/<id_payment>/
        """
        try:
            if request.method == 'GET':
                check_permission(request.user, 'view_payment')

                query = """
                    SELECT * FROM payments WHERE id_payment = %s
                """
                with connection.cursor() as cursor:
                    cursor.execute(query, [id_payment])
                    row = cursor.fetchone()
                    if row:
                        columns = [col[0] for col in cursor.description]
                        payment = dict(zip(columns, row))
                        return Response(payment, status=status.HTTP_200_OK)
                    else:
                        return Response({'detail': 'Payment not found'}, status=status.HTTP_404_NOT_FOUND)

            elif request.method == 'PUT':
                check_permission(request.user, 'update_payment')
                data = request.data

                query = """
                    UPDATE payments
                    SET id_employee = %s, id_employee_supervisor = %s, id_payment_method = %s, amount = %s,
                        payment_date = %s, extra_amount = %s, deduction_amount = %s, bonus_amount = %s,
                        payment_note = %s, src = %s, updated_at = CURRENT_TIMESTAMP
                    WHERE id_payment = %s
                """
                with connection.cursor() as cursor:
                    cursor.execute(query, [
                        data['id_employee'],
                        data['id_employee_supervisor'],
                        data['id_payment_method'],
                        data['amount'],
                        data['payment_date'],
                        data.get('extra_amount'),
                        data.get('deduction_amount'),
                        data.get('bonus_amount'),
                        data.get('payment_note'),
                        data.get('src'),
                        id_payment
                    ])

                return Response({'detail': 'Payment updated successfully'}, status=status.HTTP_200_OK)

            elif request.method == 'DELETE':
                check_permission(request.user, 'delete_payment')

                query = """
                    DELETE FROM payments WHERE id_payment = %s
                """
                with connection.cursor() as cursor:
                    cursor.execute(query, [id_payment])
                    return Response({'detail': 'Payment deleted successfully'}, status=status.HTTP_200_OK)

            return Response({'detail': f'Method {request.method} not allowed'}, status=status.HTTP_405_METHOD_NOT_ALLOWED)

        except Exception as e:
            return Response({'detail': str(e)}, status=status.HTTP_400_BAD_REQUEST)
