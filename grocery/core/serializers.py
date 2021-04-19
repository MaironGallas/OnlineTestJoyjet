from rest_framework import serializers

from grocery.core.models import Payload


class PayloadSerializer(serializers.ModelSerializer):
    class Meta:
        model = Payload
        fields = ['id', 'articles', 'carts', 'delivery_fees', 'discounts']