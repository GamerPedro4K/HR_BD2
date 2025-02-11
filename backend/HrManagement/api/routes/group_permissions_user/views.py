from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework import status
from api.utils.dotenv import is_debug_mode
from api.utils.permissions import check_permission_decorator
from django.db import connection

class GroupPermissionsViewUserSet(ViewSet):
    
    if not is_debug_mode():
        authentication_classes = [JWTAuthentication]
        permission_classes = [IsAuthenticated]

    @check_permission_decorator('view_all_permissions_user_group')
    def list(self, request):
        """
        List all employees with their groups and permissions.
        """
        order_by = request.GET.get('order_by', 'name')
        order_direction = request.GET.get('order_direction', 'ASC')
        global_search = request.GET.get('global_search', None)
        limit = request.GET.get('limit', None)
        offset = request.GET.get('offset', None)

        with connection.cursor() as cursor:
            try:
                limit = int(limit) if limit else None
                offset = int(offset) if offset else None

                query = """
                    SELECT *
                    FROM get_all_employees_groups_permissions(
                        %s::varchar,
                        ARRAY[%s]::text[],
                        ARRAY[%s]::text[],
                        %s::integer,
                        %s::integer
                    )
                """
                params = [global_search, order_by, order_direction, limit, offset]

                cursor.execute(query, params)
                rows = cursor.fetchall()

                employees = []
                total_count = rows[0][-1] if rows else 0

                import json
                for row in rows:
                    employee_data = {
                        'id_employee': row[0],
                        'src': row[1],
                        'name': row[2],
                        'groups': json.loads(row[3]) if row[3] else []
                    }
                    employees.append(employee_data)

                return Response({
                    'employees': employees,
                    'total_count': total_count
                }, status=status.HTTP_200_OK)

            except Exception as e:
                return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)