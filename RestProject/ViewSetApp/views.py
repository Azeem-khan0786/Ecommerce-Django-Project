from django.shortcuts import render,get_object_or_404
from rest_framework import status

from rest_framework.viewsets import ViewSet ,ModelViewSet
from rest_framework.response import Response
# Create your views here.
from api.models import *
from api.serializer import ProductSerializer,OrderSerializer
from .permissions import OrderPermission

class ProductViewSet(ViewSet):
    queryset = Product.objects.all()

    def list(self,request):  # to fetch all records
        serializer = ProductSerializer(self.queryset,many =True)
        return Response(serializer.data)
    
    def retrieve(self,request,pk=None):
        product_item = get_object_or_404(self.queryset,pk=pk)
        serializer = ProductSerializer(product_item)
        return Response(serializer.data)
    
    def create(self,request):
        serializer = ProductSerializer(data = request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data , status=status.HTTP_201_CREATED)
        return Response(serializer.errors , status=status.HTTP_400_BAD_REQUEST)
    
    def destroy(self,request,pk=None):
        product_item = get_object_or_404(self.queryset,pk=pk)
        product_item.is_active=False
        product_item.save()
        return Response(status=status.HTTP_204_NO_CONTENT)

    def partial_update(self,request,pk):
        product_item = get_object_or_404(self.queryset,pk=pk)
        serializer = ProductSerializer(product_item,data =request.data,partial= True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)
# ModelViewSet
class ItemModelViewSet(ModelViewSet):
    serializer_class = ProductSerializer
    queryset = Product.objects.all()

# OrderSerializer 
class OrderModelViewSet(ModelViewSet):
    serializer_class = OrderSerializer
    queryset = Order.objects.all()
    permission_classes =[OrderPermission]

