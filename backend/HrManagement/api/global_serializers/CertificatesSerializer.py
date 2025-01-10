from rest_framework import serializers

class CertificatesSerializer(serializers.Serializer):
    id_certificate_type = serializers.UUIDField(required=True)
    issuing_organization = serializers.CharField(max_length=255, required=True)
    issue_date = serializers.CharField(max_length=255, required=True)
    expiration_date = serializers.CharField(max_length=255, required=False, allow_blank=True)


class CertificatesSerializerUpdate(serializers.Serializer):
    id_certificate_type = serializers.UUIDField(required=False, allow_null=True)
    name = serializers.CharField(max_length=255, required=False, allow_blank=True)
    issuing_organization = serializers.CharField(max_length=255, required=False, allow_blank=True)
    issue_date = serializers.CharField(max_length=255, required=False, allow_blank=True)
    expiration_date = serializers.CharField(max_length=255, required=False, allow_blank=True)

