from rest_framework import serializers

class SalaryHistorySerializer(serializers.Serializer):
    base_salary = serializers.DecimalField(max_digits=10, decimal_places=2, required=False, allow_null=True)
    extra_hour_rate = serializers.DecimalField(max_digits=10, decimal_places=2, required=False, allow_null=True)
    start_date = serializers.DateField(required=True)

class SalaryHistorySerializerUpdate(serializers.Serializer):
    base_salary = serializers.DecimalField(max_digits=10, decimal_places=2, required=False, allow_null=True)
    extra_hour_rate = serializers.DecimalField(max_digits=10, decimal_places=2, required=False, allow_null=True)
    start_date = serializers.DateField(required=False, allow_null=True)