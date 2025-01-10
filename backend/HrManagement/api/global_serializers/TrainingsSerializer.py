from rest_framework import serializers

class TrainingsSerializer(serializers.Serializer):
    id_training_type = serializers.UUIDField(required=True)
    start_date = serializers.DateField(required=True)
    end_date = serializers.DateField(required=True)


class TrainingsSerializerUpdate(serializers.Serializer):
    id_training_type = serializers.UUIDField(required=False, allow_null=True)
    start_date = serializers.DateField(required=False, allow_null=True)
    end_date = serializers.DateField(required=False, allow_null=True)