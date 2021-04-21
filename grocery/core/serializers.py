from rest_framework import serializers

from grocery.core.models import Payload

# Creating a Serializer class
class PayloadSerializerLevel1(serializers.ModelSerializer):
    class Meta:
        model = Payload
        fields = ['id', 'articles', 'carts']


class PayloadSerializerLevel2(serializers.ModelSerializer):
    class Meta:
        model = Payload
        fields = ['id', 'articles', 'carts', 'delivery_fees']


class PayloadSerializerLevel3(serializers.ModelSerializer):
    class Meta:
        model = Payload
        fields = ['id', 'articles', 'carts', 'delivery_fees', 'discounts']