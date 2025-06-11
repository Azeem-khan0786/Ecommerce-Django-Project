
from api.serializer import ProductSerializer ,OrderSerializer
from api.models import Product ,Order
from rest_framework.generics import GenericAPIView
from rest_framework.mixins import RetrieveModelMixin,UpdateModelMixin,CreateModelMixin,ListModelMixin
from rest_framework.response import Response
from rest_framework import status

# Create your GenericAPIView here.
class ProductGenericAPIView(GenericAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    lookup_field  ='pk'

    # get method
    def get(self, request, *args, **kwargs):
        pk = kwargs.get('pk')
        if pk is not None:
            instance = self.get_object()
            serializer = self.get_serializer(instance)
        else:
            queryset = self.get_queryset()
            serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)
    
    def post(self,request,*args,**kargs):
        serializer = self.get_serializer(data= request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors)
    
    def put(self,request,*args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance,data= request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors)
    
    def delete(self,request,*args, **kwargs):
        instance = self.get_object()
        instance.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)



# Create your Mixins here with GenericAPIView.
class CreateReadUpdateMixins(RetrieveModelMixin,UpdateModelMixin,CreateModelMixin,ListModelMixin,GenericAPIView):
     
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    lookup_field = 'pk'

    def get(self,request,*args, **kwargs):
        pk= kwargs.get('pk')
        if pk is not None:
           return self.retrieve(self,request,*args, **kwargs)
        else:
            return self.list(self,request,*args, **kwargs)
    
    def post(self,request,*args, **kwargs):
        return self.create(self,request,*args, **kwargs)
    def patch(self, request, *args, **kwargs):
        return self.partial_update(request, *args, **kwargs)

    def delete(self, request, *args, **kwargs):
        return self.destroy(request, *args, **kwargs)
    
    
        

