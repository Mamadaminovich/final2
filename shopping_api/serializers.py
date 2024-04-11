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
        
class ShopCardSerializer(serializers.ModelSerializer):
    items = serializers.PrimaryKeyRelatedField(many=True, queryset=Item.objects.all())

    class Meta:
        model = ShopCard
        fields = ['id', 'customer', 'created_at', 'items']

    def create(self, validated_data):
        items_data = validated_data.pop('items', [])
        try:
            shop_card = ShopCard.objects.create(**validated_data)
            for item_data in items_data:
                Item.objects.create(shop_card=shop_card, **item_data)
            return shop_card
        except Exception as e:
            raise serializers.ValidationError(str(e))

    def update(self, instance, validated_data):
        items_data = validated_data.pop('items', [])
        instance.customer = validated_data.get('customer', instance.customer)
        instance.created_at = validated_data.get('created_at', instance.created_at)
        instance.save()

        # Update or create items
        instance.items.all().delete()  # Remove existing items
        for item_data in items_data:
            Item.objects.create(shop_card=instance, **item_data)

        return instance
        
class ItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = Item
        fields = '__all__'

    def create(self, validated_data):
        try:
            return Item.objects.create(**validated_data)
        except Exception as e:
            raise serializers.ValidationError(str(e))

    def update(self, instance, validated_data):
        instance.product = validated_data.get('product', instance.product)
        instance.quantity = validated_data.get('quantity', instance.quantity)
        instance.shop_card = validated_data.get('shop_card', instance.shop_card)
        instance.save()
        return instance
        
class CustomerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Customer
        fields = '__all__'

class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = '__all__'

class PurchaseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Purchase
        fields = '__all__'