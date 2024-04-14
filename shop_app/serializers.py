from rest_framework import serializers
from .models import *
class AdminSerializer(serializers.ModelSerializer):
    class Meta:
        model = Admin
        fields = '__all__'

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'
        
class CustomerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Customer
        fields = '__all__'

class ProductSerializer(serializers.ModelSerializer):
    category = serializers.PrimaryKeyRelatedField(queryset=Category.objects.all())

    class Meta:
        model = Product
        fields = '__all__'

    def create(self, validated_data):
        return Product.objects.create(**validated_data)
        
class ItemSerializer(serializers.ModelSerializer):
    product_name = serializers.SerializerMethodField()  # Add this field to store product name

    class Meta:
        model = Item
        fields = '__all__'

    def get_product_name(self, instance):
        return instance.product.name  # Retrieve the product's name from the related Product object

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation['product'] = representation.pop('product_name')  # Replace 'product' field with 'product_name'
        return representation

    def validate_quantity(self, value):
        if value <= 0:
            raise serializers.ValidationError("Quantity must be a positive integer")
        return value
    
class ShopCardSerializer(serializers.ModelSerializer):
    items = ItemSerializer(many=True, required=False)
    customer_name = serializers.SerializerMethodField()

    class Meta:
        model = ShopCard
        fields = '__all__'

    def get_customer_name(self, instance):
        return instance.customer.name 

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation['customer'] = representation.pop('customer_name')
        return representation

    def update(self, instance, validated_data):
        items_data = validated_data.pop('items', [])
        instance.customer = validated_data.get('customer', instance.customer)
        instance.created_at = validated_data.get('created_at', instance.created_at)
        instance.save()

        for item_data in items_data:
            item_id = item_data.get('id', None)
            if item_id:
                item = Item.objects.get(id=item_id, shop_card=instance)
                item.quantity = item_data.get('quantity', item.quantity)
                item.save()
            else:
                Item.objects.create(shop_card=instance, **item_data)
        return instance
    
class PurchaseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Purchase
        fields = '__all__'
