from rest_framework import serializers

from payments import models


class PaymentSerializer(serializers.ModelSerializer):
    id = serializers.ReadOnlyField()
    order_id = serializers.IntegerField(source='order.id')

    class Meta:
        model = models.Payment
        fields = ('id', 'order_id', 'session_id')
