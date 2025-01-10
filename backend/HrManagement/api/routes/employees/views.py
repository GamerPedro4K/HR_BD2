import pprint
from uuid import UUID
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication
from api.utils.dotenv import is_debug_mode 

from django.db import connection
from rest_framework import viewsets
from rest_framework.decorators import action
from django.contrib.auth.models import User
from django.contrib.auth.models import Permission
from django.contrib.auth.models import Group
from api.utils.permissions import check_permission_decorator

from .serializers import UpdateSerializer

class EmployeeInstanceMock:
    def __init__(self, id_auth_user, id_employee):
        self.id_auth_user = id_auth_user
        if isinstance(id_employee, UUID):
            self.id_employee = id_employee
        else:
            self.id_employee = UUID(id_employee)

class EmployeeViewSet(viewsets.ViewSet):
    serializer_class = UpdateSerializer

    """ 
    lists all employees
    /employees/
    """
    if not is_debug_mode():
        authentication_classes = [JWTAuthentication]
        permission_classes = [IsAuthenticated]
        
    @check_permission_decorator('view_all_employees')
    def list(self, request):
        name = request.GET.get('name', None)
        id_param = request.GET.get('id', None)
        department_id = request.GET.get('department_id', None)
        role_id = request.GET.get('role_id', None)
        status_id = request.GET.get('status_id', None)
        order_by = request.GET.get('order_by', 'first_name')
        order_direction = request.GET.get('order_direction', 'ASC')
        
        limit = int(request.GET.get('limit', 5))
        offset = int(request.GET.get('offset', 0))
        
        global_search = request.GET.get('global_search', None)
        global_search = None if global_search == '' else global_search

        with connection.cursor() as cursor:
            try:
                cursor.execute(
                    """
                    SELECT *
                        FROM get_all_employees(
                            %s,    -- name_param
                            %s,    -- id_param
                            %s,    -- department_id_param
                            %s,    -- role_param
                            %s,    -- status_param
                            ARRAY[%s]::text[],   -- order_by_param
                            ARRAY[%s]::text[],  -- order_direction_param
                            %s::varchar    -- global_search_param
                        )
                        LIMIT %s
                        OFFSET %s;
                    """,
                    [name, id_param, department_id, role_id, status_id, order_by, order_direction, global_search, limit, offset]
                )
                rows = cursor.fetchall()

                employee_data = [
                    {
                        'id': emp[0],
                        'employee_name': emp[1],
                        'role_name': emp[2],
                        'role_hex_color': emp[3],
                        'department_name': emp[4],
                        'state_name': emp[5],
                        'state_icon': emp[6],
                        'state_hex_color': emp[7]
                    }
                    for emp in rows
                ]
                
                cursor.execute(
                    """
                    SELECT count(*)
                        FROM get_all_employees(
                            %s,    -- name_param
                            %s,    -- id_param
                            %s,    -- department_id_param
                            %s,    -- role_param
                            %s,    -- status_param
                            ARRAY[%s]::text[],   -- order_by_param
                            ARRAY[%s]::text[],  -- order_direction_param
                            %s::varchar    -- global_search_param
                        );
                    """,
                    [name, id_param, department_id, role_id, status_id, order_by, order_direction, global_search]
                )
                total_count = cursor.fetchone()[0]
            except Exception as e:
                return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)
            
        return Response({
            'employees': employee_data,
            'total_count': total_count,
        }, status=status.HTTP_200_OK)
    
    """ 
    retrieve an employee by id
    /employees/{id} 
    """
    @check_permission_decorator('view_employee')
    def retrieve(self, request, pk=None):
        with connection.cursor() as cursor:
            try:
                # Retrieve employee details
                cursor.execute(
                    """
                    SELECT * FROM get_employees_by_id(%s)
                    ;
                    """,
                    [pk]
                )
                employee = cursor.fetchone()

                if not employee:
                    return Response({'error': 'Employee not found'}, status=status.HTTP_404_NOT_FOUND)

                # Retrieve latest contract
                cursor.execute(
                    """
                    SELECT c.id_contract, c.created_at, c.updated_at, ct.id_contract_type, ct.contract_type_name, ct.description
                    FROM contract c
                    INNER JOIN contract_type ct ON c.id_contract_type = ct.id_contract_type
                    WHERE c.id_employee = %s
                    ORDER BY c.created_at DESC
                    LIMIT 1;
                    """,
                    [pk]
                )
                contract = cursor.fetchone()

                # Retrieve contract state history
                cursor.execute(
                    """
                    SELECT csc.id_contract_state_contract, csc.id_contract_state, cs.state, cs.description, cs.hex_color, cs.icon
                    FROM contract_state_contract csc
                    INNER JOIN contract_state cs ON csc.id_contract_state = cs.id_contract_state
                    WHERE csc.id_contract = %s
                    ORDER BY csc.created_at DESC
                    LIMIT 1;
                    """,
                    [contract[0]] if contract else [None]
                )
                contract_state = cursor.fetchone()

                # Retrieve trainings
                cursor.execute(
                    """
                    SELECT t.id_training, t.start_date, t.end_date, tt.id_training_type, tt.name, tt.description, tt.hours
                    FROM trainings t
                    INNER JOIN training_types tt ON t.id_training_type = tt.id_training_type
                    WHERE t.id_employee = %s;
                    """,
                    [pk]
                )
                trainings = cursor.fetchall()

                # Retrieve certifications
                cursor.execute(
                    """
                    SELECT c.id_certification, c.issue_date, c.expiration_date, ct.id_certificate_type, ct.name, ct.description, c.issuing_organization, ct.icon, ct.hex_color
                    FROM certifications c
                    INNER JOIN certificate_types ct ON c.id_certificate_type = ct.id_certificate_type
                    WHERE c.id_employee = %s;
                    """,
                    [pk]
                )
                certifications = cursor.fetchall()

                # Retrieve department details
                cursor.execute(
                    """
                    SELECT d.*
                    FROM departments d
                    INNER JOIN roles r ON d.id_department = r.id_department
                    WHERE r.id_role = %s;
                    """,
                    [employee[7]]
                )
                department = cursor.fetchone()

                # Retrive salary details
                cursor.execute(
                    """
                    SELECT latest_salary_materialized_view.id_salary_history, latest_salary_materialized_view.id_employee_aproved_by, latest_salary_materialized_view.base_salary, latest_salary_materialized_view.extra_hour_rate, latest_salary_materialized_view.start_date
                    FROM latest_salary_materialized_view
                    WHERE id_contract = %s
                    ORDER BY created_at DESC
                    LIMIT 1;
                    """,
                    [contract[0]] if contract else [None]
                )
                salary = cursor.fetchone()

            except Exception as e:
                return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)

        # Organize data into structured JSON
        employee_data = {
            'id_employee': employee[0],
            'employee_name': employee[1],
            'phone': employee[2],
            'photo': employee[3],
            'email': employee[4],
            'birth_date': employee[5],
            'date_joined': employee[6],
            'location': {
                'city': employee[16],
                'country': employee[17],
                'district': employee[18],
                'address': employee[19],
                'zip_code': employee[20],
            },
            'contract': {
                'id_contract': contract[0],
                'created_at': contract[1],
                'salary': {
                    'id:_salary': salary[0],
                    'id_aproved_by': salary[1],
                    'base_salary': salary[2],
                    'extra_hour_rate': salary[3],
                    'start_date': salary[4],
                },
                'contract_type': {
                    'id_contract_type': contract[3],
                    'contract_type_name': contract[4],
                    'description': contract[5],
                },
                'contract_state': {
                    'id_contract_state_contract': contract_state[0],
                    'id_contract_state': contract_state[1],
                    'state_name': contract_state[2],
                    'description': contract_state[3],
                    'hex_color': contract_state[4],
                    'icon': contract_state[5],
                },
                'role': {
                    'id_role': employee[7],
                    'role_name': employee[8],
                    'hex_color': employee[9],
                    'description': employee[10],
                },
                'department': {
                    'id_department': department[0],
                    'department_name': department[1],
                    'description': department[2],
                },
                'created_at': contract[1],
            },
            'trainings': [
                {
                    'id_training': training[0],
                    'start_date': training[1],
                    'end_date': training[2],
                    'training_type': {
                        'id_training_type': training[3],
                        'training_type_name': training[4],
                        'description': training[5],
                        'hours': training[6],
                    }
                } for training in trainings
            ],
            'certifications': [
                {
                    'id_certification': cert[0],
                    'issue_date': cert[1],
                    'expiration_date': cert[2],
                    'certificate_type': {
                        'id_certificate_type': cert[3],
                        'certificate_type_name': cert[4],
                        'description': cert[5],
                        'icon': cert[7],
                        'hex_color': cert[8],
                    },
                    'issuing_organization': cert[6],
                } for cert in certifications
            ]
        }

        return Response(employee_data, status=status.HTTP_200_OK)

        
    """ 
    Update an employee by id
    /employees/{id} 
    """
    def update(self, request, pk=None):
        with connection.cursor() as cursor:
            cursor.execute("SELECT id_auth_user, id_employee FROM employees WHERE id_employee = %s", [pk])
            row = cursor.fetchone()
            if not row:
                return Response({"error": "Employee not found"}, status=status.HTTP_404_NOT_FOUND)
            id_auth_user, id_employee = row

        instance = EmployeeInstanceMock(id_auth_user, id_employee)

        serializer = UpdateSerializer(data=request.data, instance=instance)
        if serializer.is_valid():
            data = serializer.save()
            return Response(data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    """ 
    retrieve an employee's contracts by id
    /employees/{id}/contracts/
    """
    @action (detail=True, methods=['get'], url_path='contracts')
    def get_contracts(self, request, pk=None):
        id_contract = request.GET.get('id_contract', None)
        role_name = request.GET.get('role_name', None)
        department_name = request.GET.get('department_name', None)
        contract_type_name = request.GET.get('contract_type_name', None)
        contract_state_name = request.GET.get('contract_state_name', None)
        order_by = request.GET.getlist('order_by', 'created_at')
        order_direction = request.GET.getlist('order_direction', 'DESC')
        
        limit = int(request.GET.get('limit', 5))
        offset = int(request.GET.get('offset', 0))
        
        global_search = request.GET.get('global_search', None)
        global_search = None if global_search == '' else global_search


        with connection.cursor() as cursor:
            
            try:
                cursor.execute(
                    """
                     SELECT * FROM get_contracts(
                        %s, %s, %s, %s, %s, %s, %s, ARRAY[%s]::text[], ARRAY[%s]::text[]
                    )
                    LIMIT %s
                    OFFSET %s;
                    """,
                    [pk, global_search, id_contract, role_name, department_name, contract_type_name, contract_state_name, order_by, order_direction, limit, offset]
                )
                contracts = cursor.fetchall()
            except Exception as e:
                return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)
            
        return Response({
            'contracts': [
                {
                    'id_contract': contract[0],
                    'base_salary': contract[1],
                    'extra_hour_rate': contract[2],
                    'role_name': contract[3],
                    'department_name': contract[4],
                    'created_at': contract[5],
                    'contract_type_name': contract[6],
                    'description': contract[7],
                    'benefits_eligible': contract[8],
                    'overtime_eligible': contract[9],
                    'termination_notice_period': contract[10],
                    'contract_state_name': contract[11],
                    'contract_state_icon': contract[12],
                    'contract_state_color': contract[13],
                }
                for contract in contracts
            ],
            'beneficios': [
                        
            ]
        }, status=status.HTTP_200_OK)
    
