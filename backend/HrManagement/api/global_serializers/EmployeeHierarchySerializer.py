from rest_framework import serializers

class EmployeeHierarchySerializer(serializers.Serializer):
    id_employee_superior = serializers.UUIDField(required=False)
    start_date = serializers.DateField(required=True)
    end_date = serializers.DateField(required=False, allow_null=True)

class EmployeeHierarchySerializerUpdate(serializers.Serializer):
    id_employee_superior = serializers.UUIDField(required=False, allow_null=True)
    start_date = serializers.DateField(required=False, allow_null=True)
    end_date = serializers.DateField(required=False, allow_null=True)