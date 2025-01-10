from rest_framework import serializers

class VacationsSerializer(serializers.Serializer):
    #id_employee_substitute = serializers.UUIDField(required=True)
    #aproved_by_employee_id = serializers.UUIDField(required=True)
    #aproved_date = serializers.DateField(required=True)
    start_date = serializers.DateField(required=True)
    end_date = serializers.DateField(required=True)


class VacationsSerializerUpdate(serializers.Serializer):
    #id_employee_substitute = serializers.UUIDField(required=False, allow_null=True)
    #aproved_by_employee_id = serializers.UUIDField(required=False, allow_null=True)
    #aproved_date = serializers.DateField(required=False, allow_null=True)
    start_date = serializers.DateField(required=False, allow_null=True)
    end_date = serializers.DateField(required=False, allow_null=True)