from django.shortcuts import render , get_object_or_404
from django.http import JsonResponse 
from rest_framework.response import Response
from rest_framework.decorators import api_view
from api.serializer import ProductSerializer ,OrderSerializer
from api.models import Product ,Order
from rest_framework.permissions import AllowAny ,IsAuthenticated

from rest_framework import generics
# Create your views here.
@api_view(['GET'])
def products(request):
    products = Product.objects.all()
    serializer = ProductSerializer(products,many= True)
    # return JsonResponse(serializer.data,safe = False) use for json data
    return Response(serializer.data)

@api_view(['GET'])
def single_product(request,pk):
    product = get_object_or_404(Product,pk=pk)
    serializer = ProductSerializer(product)
    # return JsonResponse(serializer.data,safe = False) use for json data
    return Response(serializer.data)

# generic view
class OrderView(generics.ListAPIView):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
    permission_classes = [IsAuthenticated]
    # lookup_url_kwargs ='order_id'

    # def get_queryset(self):
    #     user = self.request.user
    #     return Order.objects.filter(user = user)


# oder via status
class OrderViaStatus(generics.RetrieveAPIView):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
    permission_classes = [IsAuthenticated]

    # lookup_field = 'status'
    lookup_url_kwarg = 'order_status'

    # ProductSerializer
class CreateProduct(generics.CreateAPIView):
    queryset = Product.objects.all()
    serializer_class =ProductSerializer
