from django.shortcuts import render

# Create your views here.
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response

from grocery.core.business import get_total_price
from grocery.core.serializers import PayloadSerializerLevel1, PayloadSerializerLevel3, PayloadSerializerLevel2


@api_view(['POST'])
def level1(request):
    """
    This view receives request with a payload with articles and carts and responds with a JSON with carts with total
    price.
        """
    if request.method == 'POST':
        serializer = PayloadSerializerLevel1(data=request.data)
        if serializer.is_valid():
            carts_result = []
            for cart in serializer.data['carts']:
                total_cart = get_total_price(cart, serializer.data['articles'])
                carts_result.append({'id': cart['id'], 'total': total_cart})
            carts = {'carts': carts_result}
            return Response(carts, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
def level2(request):
    """
    This view receives request with a payload with articles, carts, and delivery fees and responds with a JSON with
    carts with total price using the policy of delivery fees.
    """
    if request.method == 'POST':
        serializer = PayloadSerializerLevel2(data=request.data)
        if serializer.is_valid():
            carts_result = []
            for cart in serializer.data['carts']:
                total_cart = get_total_price(cart, serializer.data['articles'], serializer.data['delivery_fees'])
                carts_result.append({'id': cart['id'], 'total': total_cart})
            carts = {'carts': carts_result}
            return Response(carts, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
def level3(request):
    """
    This view receives request with a payload with articles, carts, delivery fees, and discounts and responds with a
    JSON with carts with total price using the policy of delivery fees and the discounts if applicable.
    """
    if request.method == 'POST':
        serializer = PayloadSerializerLevel3(data=request.data)
        if serializer.is_valid():
            carts_result = []
            for cart in serializer.data['carts']:
                total_cart = get_total_price(cart, serializer.data['articles'], serializer.data['delivery_fees'],
                                             serializer.data['discounts'])
                carts_result.append({'id': cart['id'], 'total': total_cart})
            carts = {'carts': carts_result}
            return Response(carts, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)