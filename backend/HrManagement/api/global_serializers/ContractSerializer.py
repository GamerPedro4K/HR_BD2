from rest_framework import serializers

class ContractSerializer(serializers.Serializer):
    id_role = serializers.UUIDField(required=True)
    id_contract_type = serializers.UUIDField(required=True)
    id_contract_state = serializers.UUIDField(required=True)


class ContractSerializerUpdate(serializers.Serializer):
    id_role = serializers.UUIDField(required=False, allow_null=True)
    id_contract_type = serializers.UUIDField(required=False, allow_null=True)
    id_contract_state = serializers.UUIDField(required=False, allow_null=True)