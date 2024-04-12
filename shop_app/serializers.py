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
    category = CategorySerializer()  # Nested serializer for Category

    class Meta:
        model = Product
        fields = '__all__'
        
class ItemSerializer(serializers.ModelSerializer):
    product = serializers.PrimaryKeyRelatedField(queryset=Product.objects.all())
    
    class Meta:
        model = Item
        fields = '__all__'
    
    def validate_quantity(self, value):
        if value <= 0:
            raise serializers.ValidationError("Quantity must be a positive integer")
        return value
    
class ShopCardSerializer(serializers.ModelSerializer):
    items = ItemSerializer(many=True, required=False)

    class Meta:
        model = ShopCard
        fields = '__all__'

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
