from django.shortcuts import render

# Create your views here.
from api.models import Product,Order,OrderItem
from api.serializer import ProductSerializer,OrderItem,OrderItemSerializer,OrderSerializer
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.http import Http404
from rest_framework.pagination import PageNumberPagination

# create class based api
class ProductClassBasedView(APIView):
    def get (self,resqest):
          name =self.request.GET.get('name')
          price = self.request.GET.get('price')  # can be 'asc', 'desc', or a number

          products = Product.objects.all()

          # Filter by name
          if name:
               products = products.filter(name__icontains=name)

          # Filter or sort by price
          if price:
               if price == 'asc':
                    products = products.order_by('price')  # sort ascending
               elif price == 'desc':
                    products = products.order_by('-price')  # sort descending
               else:
                    try:
                         price_value = float(price)
                         products = products.filter(price=price_value)  # exact match
                    except ValueError:
                         pass  # ignore if not a number or 'asc'/'desc

          # Pagination
          paginator = PageNumberPagination()
          paginator.page_size = 5  # You can set this dynamically if you want
          result_page = paginator.paginate_queryset(products, self.request)

          serializer = ProductSerializer(result_page, many=True)
          return paginator.get_paginated_response(serializer.data)
    
    # post method to create products
    def post(self,request):
        serializer = ProductSerializer(data = request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data , status=status.HTTP_201_CREATED)
        return Response(serializer.errors , status=status.HTTP_400_BAD_REQUEST)

# ProductClassBasedViewDetails
# Class based view for all http methods to know details of Products

class ProductClassBasedViewDetails(APIView):
     
     # method to get instance of Product
      def get_project_object(self,pk):
          try:
              return Product.objects.get(pk=pk)
          except Product.ObjectDoesNotExist:
               raise Http404   
          
      def get(self,reqest,pk):
            product = self.get_project_object(pk)
            serializer = ProductSerializer(product)
            return Response(serializer.data)
      
      def put(self,request,pk):
           product = self.get_project_object(pk)
           serializer = ProductSerializer(product,data = request.data)
           if serializer.is_valid():
                serializer.save()
                return Response(serializer.data)
           return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)
      
      def patch(self,request,pk):     
           product = self.get_project_object(pk)
           serializer = ProductSerializer(product,data =request.data , partial= True)
           if serializer.is_valid():
                serializer.save()
                return Response(serializer.data)
           return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)
      def delete(self,request,pk):
           product =self.get_project_object(pk)
           product.delete()   
           return Response(status=status.HTTP_204_NO_CONTENT)