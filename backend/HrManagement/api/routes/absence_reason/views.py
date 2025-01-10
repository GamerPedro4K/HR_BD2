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

class AbsenceReasonViewSet(ViewSet):
    if not is_debug_mode():
        authentication_classes = [JWTAuthentication]
        permission_classes = [IsAuthenticated]

    """
        e.g /api/absence_reason/?employee_id=<id_employee>
        e.g /api/absence_reason/?supervisor_id=<id_supervisor>
        e.g /api/absence_reason/?substitute_id=<id_substitute>
    """
    @check_permission_decorator('view_all_absence_reasons')
    def list(self, request):
        employee_id = request.query_params.get('employee_id', None)
        supervisor_id = request.query_params.get('supervisor_id', None)
        substitute_id = request.query_params.get('substitute_id', None)

        query = """
            SELECT
                absence_reason.*,
                CAST(auth_user.first_name || ' ' || auth_user.last_name AS varchar) AS employee_name,
                CAST(supervisor.first_name || ' ' || supervisor.last_name AS varchar) AS supervisor_name,
                CAST(substitute.first_name || ' ' || substitute.last_name AS varchar) AS substitute_name
            FROM absence_reason
            INNER JOIN employees ON absence_reason.id_employee = employees.id_employee
            INNER JOIN auth_user ON employees.id_auth_user = auth_user.id
            LEFT JOIN employees AS supervisor_employee ON absence_reason.id_employee_supervisor = supervisor_employee.id_employee
            LEFT JOIN auth_user AS supervisor ON supervisor_employee.id_auth_user = supervisor.id
            LEFT JOIN employees AS substitute_employee ON absence_reason.id_employee_substitute = substitute_employee.id_employee
            LEFT JOIN auth_user AS substitute ON substitute_employee.id_auth_user = substitute.id;
        """
        if employee_id:
            query += " WHERE aabsence_reason.id_employee = %s"
            params = [employee_id]
        if supervisor_id:
            query += " WHERE absence_reason.id_employee_supervisor = %s"
            params = [supervisor_id]
        if substitute_id:
            query += " WHERE absence_reason.id_employee_substitute = %s"
            params = [substitute_id]
        else:
            params = []

        with connection.cursor() as cursor:
            cursor.execute(query, params)
            columns = [col[0] for col in cursor.description]
            absence_reasons = [dict(zip(columns, row)) for row in cursor.fetchall()]

        return Response(absence_reasons, status=status.HTTP_200_OK)

    @check_permission_decorator('create_absence_reason')
    def create(self, request):
        data = request.data
        try:
            with connection.cursor() as cursor:
                cursor.execute("""
                    INSERT INTO absence_reason (id_employee, id_employee_supervisor, id_employee_substitute, name, description, start_date, end_date)
                    VALUES (%s, %s, %s, %s, %s, %s, %s)
                    RETURNING id_absence_reason
                """, [
                    data['id_employee'],
                    data['id_employee_supervisor'],
                    data['id_employee_substitute'],
                    data['name'],
                    data['description'],
                    data['start_date'],
                    data['end_date']
                ])
                id_absence_reason = cursor.fetchone()[0]

            return Response({'id_absence_reason': id_absence_reason}, status=status.HTTP_201_CREATED)

        except Exception as e:
            return Response({'detail': str(e)}, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=False, methods=['get', 'put', 'delete'], url_path=r'(?P<id_absence_reason>[^/]+)')
    def handle(self, request, id_absence_reason):
        """
        - GET /api/absence_reason/<id_absence_reason>/
        - PUT /api/absence_reason/<id_absence_reason>/
        - DELETE /api/absence_reason/<id_absence_reason>/
        """
        try:
            if request.method == 'GET':
                check_permission(request.user, 'view_absence_reason')

                query = """
                    SELECT * FROM absence_reason WHERE id_absence_reason = %s
                """
                with connection.cursor() as cursor:
                    cursor.execute(query, [id_absence_reason])
                    row = cursor.fetchone()
                    if row:
                        columns = [col[0] for col in cursor.description]
                        absence_reason = dict(zip(columns, row))
                        return Response(absence_reason, status=status.HTTP_200_OK)
                    else:
                        return Response({'detail': 'Absence reason not found'}, status=status.HTTP_404_NOT_FOUND)

            elif request.method == 'PUT':
                check_permission(request.user, 'update_absence_reason')
                data = request.data

                query = """
                    UPDATE absence_reason
                    SET id_employee = %s, id_employee_supervisor = %s, id_employee_substitute = %s,
                        name = %s, description = %s, start_date = %s, end_date = %s, updated_at = CURRENT_TIMESTAMP
                    WHERE id_absence_reason = %s
                """
                with connection.cursor() as cursor:
                    cursor.execute(query, [
                        data['id_employee'],
                        data['id_employee_supervisor'],
                        data['id_employee_substitute'],
                        data['name'],
                        data['description'],
                        data['start_date'],
                        data['end_date'],
                        id_absence_reason
                    ])

                return Response({'detail': 'Absence reason updated successfully'}, status=status.HTTP_200_OK)

            elif request.method == 'DELETE':
                check_permission(request.user, 'delete_absence_reason')

                query = """
                    DELETE FROM absence_reason WHERE id_absence_reason = %s
                """
                with connection.cursor() as cursor:
                    cursor.execute(query, [id_absence_reason])
                    return Response({'detail': 'Absence reason deleted successfully'}, status=status.HTTP_200_OK)

            return Response({'detail': f'Method {request.method} not allowed'}, status=status.HTTP_405_METHOD_NOT_ALLOWED)

        except Exception as e:
            return Response({'detail': str(e)}, status=status.HTTP_400_BAD_REQUEST)
