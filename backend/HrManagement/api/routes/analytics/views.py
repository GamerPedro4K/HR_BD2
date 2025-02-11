from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import status
from django.db import connection
from rest_framework import serializers
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication
from api.utils.dotenv import is_debug_mode 
from api.utils.permissions import check_permission_decorator
from rest_framework.decorators import action


class AbsenceAnalyticsSerializer(serializers.Serializer):
    employee_name = serializers.CharField()
    total_absences = serializers.IntegerField()
    total_days_absent = serializers.IntegerField()


class CurrentMonthPaymentAnalyticsSerializer(serializers.Serializer):
    month_name = serializers.CharField()
    total_employees_paid = serializers.IntegerField()
    total_base_salary = serializers.DecimalField(max_digits=12, decimal_places=2)
    total_bonus_amount = serializers.DecimalField(max_digits=12, decimal_places=2)
    total_deduction_amount = serializers.DecimalField(max_digits=12, decimal_places=2)
    net_payment_amount = serializers.DecimalField(max_digits=12, decimal_places=2)
    average_payment = serializers.DecimalField(max_digits=12, decimal_places=2)
    min_payment = serializers.DecimalField(max_digits=12, decimal_places=2)
    max_payment = serializers.DecimalField(max_digits=12, decimal_places=2)
    employees_with_bonus = serializers.IntegerField()
    employees_with_deduction = serializers.IntegerField()


class SalaryByDepartmentSerializer(serializers.Serializer):
    department_name = serializers.CharField()
    employee_count = serializers.IntegerField()
    avg_salary = serializers.DecimalField(max_digits=12, decimal_places=2)
    min_salary = serializers.DecimalField(max_digits=12, decimal_places=2)
    max_salary = serializers.DecimalField(max_digits=12, decimal_places=2)


class TotalEmployeesPerDepartmentSerializer(serializers.Serializer):
    department_name = serializers.CharField()
    total_employees = serializers.IntegerField()


class AnalyticsViewSet(ViewSet):
    if not is_debug_mode():
        authentication_classes = [JWTAuthentication]
        permission_classes = [IsAuthenticated]

    def dictfetchall(self, cursor):
        """Retorna todas as linhas do cursor como dict"""
        columns = [col[0] for col in cursor.description]
        return [
            dict(zip(columns, row))
            for row in cursor.fetchall()
        ]

    @check_permission_decorator('view_analytics')
    @action(detail=False, methods=['get'])
    def absence_analytics(self, request):
        try:
            with connection.cursor() as cursor:
                cursor.execute("SELECT * FROM absence_analytics_view")
                data = self.dictfetchall(cursor)
                serializer = AbsenceAnalyticsSerializer(data=data, many=True)
                serializer.is_valid()
                return Response(serializer.data)
        except Exception as e:
            return Response(
                {'error': str(e)}, 
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

    @check_permission_decorator('view_analytics')
    @action(detail=False, methods=['get'])
    def current_month_payments(self, request):
        try:
            with connection.cursor() as cursor:
                cursor.execute("SELECT * FROM current_month_payment_analytics_view")
                data = self.dictfetchall(cursor)
                serializer = CurrentMonthPaymentAnalyticsSerializer(data=data, many=True)
                serializer.is_valid()
                return Response(serializer.data)
        except Exception as e:
            return Response(
                {'error': str(e)}, 
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

    @check_permission_decorator('view_analytics')
    @action(detail=False, methods=['get'])
    def salary_by_department(self, request):
        try:
            with connection.cursor() as cursor:
                cursor.execute("SELECT * FROM salary_by_departament_view")
                data = self.dictfetchall(cursor)
                serializer = SalaryByDepartmentSerializer(data=data, many=True)
                serializer.is_valid()
                return Response(serializer.data)
        except Exception as e:
            return Response(
                {'error': str(e)}, 
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

    @check_permission_decorator('view_analytics')
    @action(detail=False, methods=['get'])
    def employees_per_department(self, request):
        try:
            with connection.cursor() as cursor:
                cursor.execute("SELECT * FROM total_employees_per_department_view")
                data = self.dictfetchall(cursor)
                serializer = TotalEmployeesPerDepartmentSerializer(data=data, many=True)
                serializer.is_valid()
                return Response(serializer.data)
        except Exception as e:
            return Response(
                {'error': str(e)}, 
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

    @check_permission_decorator('view_analytics')
    def list(self, request):
        """
        Retorna um resumo geral para o dashboard combinando todas as views
        """
        try:
            with connection.cursor() as cursor:
                # Dados de pagamento do mês atual
                cursor.execute("SELECT * FROM current_month_payment_analytics_view")
                payment_data = self.dictfetchall(cursor)
                payment_serializer = CurrentMonthPaymentAnalyticsSerializer(data=payment_data, many=True)
                payment_serializer.is_valid()

                # Top 5 funcionários com mais ausências
                cursor.execute("SELECT * FROM absence_analytics_view")
                absence_data = self.dictfetchall(cursor)
                absence_serializer = AbsenceAnalyticsSerializer(data=absence_data, many=True)
                absence_serializer.is_valid()

                # Dados de salário por departamento
                cursor.execute("SELECT * FROM salary_by_departament_view")
                salary_data = self.dictfetchall(cursor)
                salary_serializer = SalaryByDepartmentSerializer(data=salary_data, many=True)
                salary_serializer.is_valid()

                # Total de funcionários por departamento
                cursor.execute("SELECT * FROM total_employees_per_department_view")
                dept_data = self.dictfetchall(cursor)
                dept_serializer = TotalEmployeesPerDepartmentSerializer(data=dept_data, many=True)
                dept_serializer.is_valid()

                return Response({
                    'current_month_payments': payment_serializer.data,
                    'top_absences': absence_serializer.data,
                    'department_salaries': salary_serializer.data,
                    'department_counts': dept_serializer.data
                })

        except Exception as e:
            return Response(
                {'error': str(e)}, 
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
