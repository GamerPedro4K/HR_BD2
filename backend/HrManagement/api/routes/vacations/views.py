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

class VacationsViewSet(ViewSet):
    if not is_debug_mode():
        authentication_classes = [JWTAuthentication]
        permission_classes = [IsAuthenticated]

    """
    ViewSet para manipular a tabela 'vacations'.
    e.g GET /api/vacations/?department_id=c843eb26-87d4-40d6-8540-3527589e15a8
    """

    @check_permission_decorator('view_all_vacations')
    def list(self, request):
        """
        Lista todas as férias com opção de filtrar por departamento.
        Exemplo de URL: /api/vacations/?department_id=<id_department>
        """
        department_id = request.query_params.get('department_id', None)

        query = """
            SELECT CONCAT(u.first_name, ' ', u.last_name) AS employee_name, u.email, v.*, r.id_department, d.name AS department_name
            FROM vacations v
            INNER JOIN employees e ON v.id_employee = e.id_employee
            INNER JOIN auth_user u ON e.id_auth_user = u.id
            INNER JOIN contract c ON e.id_employee = c.id_employee
            INNER JOIN roles r ON c.id_role = r.id_role
            INNER JOIN departments d ON r.id_department = d.id_department
        """
        if department_id:
            query += " WHERE r.id_department = %s"
            params = [department_id]
        else:
            params = []

        with connection.cursor() as cursor:
            cursor.execute(query, params)
            columns = [col[0] for col in cursor.description] # description is metadata about the columns 
            vacations = [dict(zip(columns, row)) for row in cursor.fetchall()]

        return Response(vacations, status=status.HTTP_200_OK)

    @check_permission_decorator('create_vacation')
    def create(self, request):
        """
        Cria um novo registro de férias.
        """
        data = request.data
        try:
            with connection.cursor() as cursor:
                cursor.execute("""
                    INSERT INTO vacations (id_employee, aproved_date, start_date, end_date)
                    VALUES (%s, %s, %s, %s)
                    RETURNING id_vacation
                """, [
                    data['id_employee'],
                    data['aproved_date'],
                    data['start_date'],
                    data['end_date']
                ])
                id_vacation = cursor.fetchone()[0]

            return Response({'id_vacation': id_vacation}, status=status.HTTP_201_CREATED)

        except Exception as e:
            return Response({'detail': str(e)}, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=False, methods=['get', 'put', 'delete'], url_path=r'(?P<id_vacation>[^/]+)')
    def handle(self, request, id_vacation):
        """
        Lida com operações GET, PUT e DELETE em um único endpoint para a tabela 'vacations'.
        Exemplo de URLs:
        - GET /api/vacations/<id_vacation>/
        - PUT /api/vacations/<id_vacation>/
        - DELETE /api/vacations/<id_vacation>/
        """
        try:
            if request.method == 'GET':
                check_permission(request.user, 'view_vacation')

                query = """
                    SELECT * FROM vacations WHERE id_vacation = %s
                """
                with connection.cursor() as cursor:
                    cursor.execute(query, [id_vacation])
                    row = cursor.fetchone()
                    if row:
                        columns = [col[0] for col in cursor.description]
                        vacation = dict(zip(columns, row))
                        return Response(vacation, status=status.HTTP_200_OK)
                    else:
                        return Response({'detail': 'Vacation not found'}, status=status.HTTP_404_NOT_FOUND)

            elif request.method == 'PUT':
                check_permission(request.user, 'update_vacation')
                data = request.data

                query = """
                    UPDATE vacations
                    SET id_employee = %s, 
                        aproved_date = %s, start_date = %s, end_date = %s, updated_at = CURRENT_TIMESTAMP
                    WHERE id_vacation = %s
                """
                with connection.cursor() as cursor:
                    cursor.execute(query, [
                        data['id_employee'],
                        data['aproved_date'],
                        data['start_date'],
                        data['end_date'],
                        id_vacation
                    ])

                return Response({'detail': 'Vacation updated successfully'}, status=status.HTTP_200_OK)

            elif request.method == 'DELETE':
                check_permission(request.user, 'delete_vacation')

                query = """
                    DELETE FROM vacations WHERE id_vacation = %s
                """
                with connection.cursor() as cursor:
                    cursor.execute(query, [id_vacation])
                    return Response({'detail': 'Vacation deleted successfully'}, status=status.HTTP_200_OK)

            return Response({'detail': f'Method {request.method} not allowed'}, status=status.HTTP_405_METHOD_NOT_ALLOWED)

        except Exception as e:
            return Response({'detail': str(e)}, status=status.HTTP_400_BAD_REQUEST)
