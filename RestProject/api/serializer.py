from  rest_framework import serializers
from api.models import Product,Order ,OrderItem


class OrderItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderItem
        fields = ['product','quantity','item_subtotal']

class OrderSerializer(serializers.ModelSerializer):
    items = OrderItemSerializer(many=True,read_only= True)
    class Meta:
        model = Order
        fields = '__all__' 

class ProductSerializer(serializers.ModelSerializer):
    # orders = serializers.StringRelatedField(many=True) # for string method
    # orders =  OrderSerializer(many=True, read_only=True)
    # orders = serializers.PrimaryKeyRelatedField(read_only= True,many=True)
    
    class Meta:
        model = Product
        fields =( 'id','name','description','price','stock','orders',)

    # validate_<field> for model field validation
    def validate_price(self,value):
        if value<5:
            raise serializers.ValidationError('Price must be greater then  5')
        return value
    # Object-Level Validation
    def validate(self,data):
        if data['name'] == data['description']:
            raise serializers.ValidationError('Name can`t be enter into the Description box ')    
        return data  
