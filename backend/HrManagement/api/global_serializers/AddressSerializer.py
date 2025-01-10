from rest_framework import serializers

class AddressSerializer(serializers.Serializer):
    street = serializers.CharField(max_length=200, required=True)
    zip_code = serializers.CharField(max_length=8, required=True)
    city = serializers.CharField(max_length=100, required=True)
    district = serializers.CharField(max_length=20, required=True)
    country = serializers.CharField(max_length=2, required=True)


class AddressSerializerUpdate(serializers.Serializer):
    street = serializers.CharField(max_length=200, required=False, allow_blank=True)
    zip_code = serializers.CharField(max_length=8, required=False, allow_blank=True)
    city = serializers.CharField(max_length=100, required=False, allow_blank=True)
    district = serializers.CharField(max_length=20, required=False, allow_blank=True)
    country = serializers.CharField(max_length=2, required=False, allow_blank=True)
