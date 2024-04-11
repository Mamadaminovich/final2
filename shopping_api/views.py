from django.shortcuts import render
from rest_framework import generics
from .models import *
from .serializers import *
from rest_framework.permissions import IsAuthenticated
from django.db.models import Sum, Count
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from datetime import datetime, timedelta


class ModelListCreateAPIView(generics.ListCreateAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = None
    queryset = None

class ModelRetrieveUpdateDestroyAPIView(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = None  
    queryset = None

# Admin views
class AdminListCreateAPIView(ModelListCreateAPIView):
    serializer_class = AdminSerializer
    queryset = Admin.objects.all()

class AdminRetrieveUpdateDestroyAPIView(ModelRetrieveUpdateDestroyAPIView):
    serializer_class = AdminSerializer
    queryset = Admin.objects.all()

# Category views
class CategoryListCreateAPIView(ModelListCreateAPIView):
    serializer_class = CategorySerializer
    queryset = Category.objects.all()

class CategoryRetrieveUpdateDestroyAPIView(ModelRetrieveUpdateDestroyAPIView):
    serializer_class = CategorySerializer
    queryset = Category.objects.all()

# Customer views
class CustomerListCreateAPIView(generics.ListCreateAPIView):
    queryset = Customer.objects.all()
    serializer_class = CustomerSerializer

class CustomerRetrieveUpdateDestroyAPIView(ModelRetrieveUpdateDestroyAPIView):
    serializer_class = CustomerSerializer
    queryset = Customer.objects.all()

# Product views
class ProductListCreateAPIView(ModelListCreateAPIView):
    serializer_class = ProductSerializer
    queryset = Product.objects.all()

class ProductRetrieveUpdateDestroyAPIView(ModelRetrieveUpdateDestroyAPIView):
    serializer_class = ProductSerializer
    queryset = Product.objects.all()

# ShopCard views
class ShopCardListCreateAPIView(ModelListCreateAPIView):
    serializer_class = ShopCardSerializer
    queryset = ShopCard.objects.all()

class ShopCardRetrieveUpdateDestroyAPIView(ModelRetrieveUpdateDestroyAPIView):
    serializer_class = ShopCardSerializer
    queryset = ShopCard.objects.all()

# Item views
class ItemsListCreateAPIView(generics.ListCreateAPIView):
    queryset = Item.objects.all()
    serializer_class = ItemSerializer
    
# class ItemsListCreateAPIView(ModelListCreateAPIView):
#     serializer_class = ItemSerializer
#     queryset = Item.objects.all()

class ItemsRetrieveUpdateDestroyAPIView(ModelRetrieveUpdateDestroyAPIView):
    serializer_class = ItemSerializer
    queryset = Item.objects.all()

class PurchaseHistoryAPIView(generics.ListAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = PurchaseSerializer

    def get_queryset(self):
        customer_id = self.kwargs['customer_id']
        return Purchase.objects.filter(customer_id=customer_id)
    
class CheckTotalPurchase(APIView):
    def get(self, request, customer_id):
        total_purchase = Purchase.objects.filter(customer_id=customer_id).aggregate(Sum('quantity'))['quantity__sum']
        if total_purchase and total_purchase > 1000000:
            return Response({'message': 'Total purchase exceeds $1000000'}, status=status.HTTP_200_OK)
        else:
            return Response({'message': 'Total purchase does not exceed $1000000'}, status=status.HTTP_400_BAD_REQUEST)
        
class TotalProducts(APIView):
    def get(self, request):
        total_products = Product.objects.count()
        return Response({'total_products': total_products}, status=status.HTTP_200_OK)
    
class ExpiredProducts(APIView):
    def get(self, request):
        threshold_date = datetime.now() - timedelta(days=30)
        expired_products = Product.objects.filter(purchase__purchase_date__lte=threshold_date)
        serialized_products = ProductSerializer(expired_products, many=True)
        return Response(serialized_products.data, status=status.HTTP_200_OK)
    
class MostSoldProduct(APIView):
    def get(self, request):
        most_sold_product = Product.objects.annotate(total_sales=Count('purchase')).order_by('-total_sales').first()
        if most_sold_product:
            
            serialized_product = ProductSerializer(most_sold_product)
            return Response(serialized_product.data, status=status.HTTP_200_OK)
        else:
            return Response({'message': 'No product found'}, status=status.HTTP_404_NOT_FOUND)
        
class OptionalUserRequest(APIView):
    def post(self, request):
        if 'optional_user' in request.data:
            optional_user_data = request.data['optional_user']
            print("Optional User Data:", optional_user_data)
            return Response({'message': 'Request processed successfully with optional user'}, status=status.HTTP_200_OK)
        else:
            return Response({'error': 'Optional user data not provided'}, status=status.HTTP_400_BAD_REQUEST)
        
class PurchaseView(APIView):
    def post(self, request):
        customer_id = request.data.get('customer_id')
        product_id = request.data.get('product_id')
        quantity = request.data.get('quantity')

        try:
            customer = Customer.objects.get(pk=customer_id)
            product = Product.objects.get(pk=product_id)
        except (Customer.DoesNotExist, Product.DoesNotExist):
            return Response({'error': 'Customer or product not found'}, status=status.HTTP_404_NOT_FOUND)

        if customer.make_purchase(product, quantity):
            Purchase.objects.create(customer=customer, product=product, quantity=quantity)
            return Response({'message': 'Purchase successful'}, status=status.HTTP_201_CREATED)
        else:
            return Response({'error': 'Insufficient balance'}, status=status.HTTP_400_BAD_REQUEST)

def home(request):
    return render(request, 'index.html', {})





