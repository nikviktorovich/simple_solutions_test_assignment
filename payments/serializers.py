from rest_framework import serializers

from payments import models


class PaymentSerializer(serializers.ModelSerializer):
    id = serializers.ReadOnlyField()
    item_id = serializers.IntegerField(source='item.id')

    class Meta:
        model = models.Payment
        fields = ('id', 'item_id', 'session_id')
