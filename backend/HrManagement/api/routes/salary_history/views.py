from rest_framework.viewsets import ViewSet
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import status
from django.db import connection

from api.utils.dotenv import is_debug_mode
from api.utils.permissions import check_permission_decorator, check_permission
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication

class SalaryHistoryViewSet(ViewSet):
    if not is_debug_mode():
        authentication_classes = [JWTAuthentication]
        permission_classes = [IsAuthenticated]

    """
        /api/salary_history/?id_contract=<id_contract>
        /api/salary_history/?id_employee=<id_employee>
    """
    @check_permission_decorator('view_all_salary_history')
    def list(self, request):
        id_contract = request.query_params.get('id_contract', None)
        id_employee = request.query_params.get('id_employee', None)

        query = """
            SELECT sh.*, c.id_contract, c.id_employee
            FROM salary_history sh
            INNER JOIN contract c ON sh.id_contract = c.id_contract
        """
        params = []
        conditions = []

        if id_contract:
            conditions.append("c.id_contract = %s")
            params.append(id_contract)
        if id_employee:
            conditions.append("c.id_employee = %s")
            params.append(id_employee)

        if conditions:
            query += " WHERE " + " AND ".join(conditions)

        query += " ORDER BY sh.created_at DESC"

        with connection.cursor() as cursor:
            cursor.execute(query, params)
            columns = [col[0] for col in cursor.description]
            salary_history = [dict(zip(columns, row)) for row in cursor.fetchall()]

        return Response(salary_history, status=status.HTTP_200_OK)

    @check_permission_decorator('create_salary_history')
    def create(self, request):
        data = request.data
        try:
            with connection.cursor() as cursor:
                cursor.execute("""
                    INSERT INTO salary_history (id_contract, id_employee_aproved_by, base_salary, extra_hour_rate, start_date)
                    VALUES (%s, %s, %s, %s, %s)
                    RETURNING id_salary_history
                """, [
                    data['id_contract'],
                    data['id_employee_aproved_by'],
                    data['base_salary'],
                    data['extra_hour_rate'],
                    data['start_date']
                ])
                id_salary_history = cursor.fetchone()[0]

            return Response({'id_salary_history': id_salary_history}, status=status.HTTP_201_CREATED)

        except Exception as e:
            return Response({'detail': str(e)}, status=status.HTTP_400_BAD_REQUEST)

    """
    - GET /api/salary_history/<id_salary_history>/
    - PUT /api/salary_history/<id_salary_history>/
    - DELETE /api/salary_history/<id_salary_history>/
    """
    @action(detail=False, methods=['get', 'put', 'delete'], url_path=r'(?P<id_salary_history>[^/]+)')
    def handle(self, request, id_salary_history):
        try:
            if request.method == 'GET':
                check_permission(request.user, 'view_salary_history')

                query = """
                    SELECT * FROM salary_history WHERE id_salary_history = %s
                """
                with connection.cursor() as cursor:
                    cursor.execute(query, [id_salary_history])
                    row = cursor.fetchone()
                    if row:
                        columns = [col[0] for col in cursor.description]
                        salary_history = dict(zip(columns, row))
                        return Response(salary_history, status=status.HTTP_200_OK)
                    else:
                        return Response({'detail': 'Salary history not found'}, status=status.HTTP_404_NOT_FOUND)

            elif request.method == 'PUT':
                check_permission(request.user, 'update_salary_history')
                data = request.data

                query = """
                    UPDATE salary_history
                    SET id_contract = %s, id_employee_aproved_by = %s, base_salary = %s, extra_hour_rate = %s,
                        start_date = %s, updated_at = CURRENT_TIMESTAMP
                    WHERE id_salary_history = %s
                """
                with connection.cursor() as cursor:
                    cursor.execute(query, [
                        data['id_contract'],
                        data['id_employee_aproved_by'],
                        data['base_salary'],
                        data['extra_hour_rate'],
                        data['start_date'],
                        id_salary_history
                    ])

                return Response({'detail': 'Salary history updated successfully'}, status=status.HTTP_200_OK)

            elif request.method == 'DELETE':
                check_permission(request.user, 'delete_salary_history')

                query = """
                    DELETE FROM salary_history WHERE id_salary_history = %s
                """
                with connection.cursor() as cursor:
                    cursor.execute(query, [id_salary_history])
                    return Response({'detail': 'Salary history deleted successfully'}, status=status.HTTP_200_OK)

            return Response({'detail': f'Method {request.method} not allowed'}, status=status.HTTP_405_METHOD_NOT_ALLOWED)

        except Exception as e:
            return Response({'detail': str(e)}, status=status.HTTP_400_BAD_REQUEST)
