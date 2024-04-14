from django.shortcuts import render
from rest_framework import generics
from .models import *
from .serializers import *
from rest_framework.permissions import IsAuthenticated
from django.db.models import Sum, Count
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.utils import timezone
from rest_framework.decorators import api_view, permission_classes
from django.shortcuts import get_object_or_404
from rest_framework.exceptions import ValidationError
from .permissions import IsAuthenticatedAndAdminOrReadOnly


class ModelListCreateAPIView(generics.ListCreateAPIView):
    permission_classes = [IsAuthenticatedAndAdminOrReadOnly]
    serializer_class = None
    queryset = None

class ModelRetrieveUpdateDestroyAPIView(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [IsAuthenticatedAndAdminOrReadOnly]
    serializer_class = None
    queryset = None

class AdminListCreateAPIView(generics.ListCreateAPIView):
    queryset = Admin.objects.all()
    serializer_class = AdminSerializer
    permission_classes = [IsAuthenticatedAndAdminOrReadOnly]

class AdminRetrieveUpdateDestroyAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Admin.objects.all()
    serializer_class = AdminSerializer
    permission_classes = [IsAuthenticatedAndAdminOrReadOnly]

class CategoryListCreateAPIView(generics.ListCreateAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer

class CategoryRetrieveUpdateDestroyAPIView(ModelRetrieveUpdateDestroyAPIView):
    serializer_class = CategorySerializer
    queryset = Category.objects.all()

class CustomerListCreateAPIView(generics.ListCreateAPIView):
    queryset = Customer.objects.all()
    serializer_class = CustomerSerializer

class CustomerRetrieveUpdateDestroyAPIView(ModelRetrieveUpdateDestroyAPIView):
    serializer_class = CustomerSerializer
    queryset = Customer.objects.all()

class ProductListCreateAPIView(ModelListCreateAPIView):
    serializer_class = ProductSerializer
    queryset = Product.objects.all()

class ProductRetrieveUpdateDestroyAPIView(ModelRetrieveUpdateDestroyAPIView):
    serializer_class = ProductSerializer
    queryset = Product.objects.all()

class ItemsListCreateAPIView(generics.ListCreateAPIView):
    queryset = Item.objects.all()
    serializer_class = ItemSerializer

class ItemsRetrieveUpdateDestroyAPIView(ModelRetrieveUpdateDestroyAPIView):
    serializer_class = ItemSerializer
    queryset = Item.objects.all()

class ShopCardListCreateAPIView(generics.ListCreateAPIView):
    queryset = ShopCard.objects.all()
    serializer_class = ShopCardSerializer
    permission_classes = [IsAuthenticatedAndAdminOrReadOnly]

class ShopCardRetrieveUpdateDestroyAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = ShopCard.objects.all()
    serializer_class = ShopCardSerializer
    permission_classes = [IsAuthenticatedAndAdminOrReadOnly]


class ModelListCreateAPIView(generics.ListCreateAPIView):
    permission_classes = [IsAuthenticatedAndAdminOrReadOnly]
    serializer_class = None
    queryset = None

class ModelRetrieveUpdateDestroyAPIView(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [IsAuthenticatedAndAdminOrReadOnly]
    serializer_class = None
    queryset = None

class AdminListCreateAPIView(generics.ListCreateAPIView):
    queryset = Admin.objects.all()
    serializer_class = AdminSerializer
    permission_classes = [IsAuthenticatedAndAdminOrReadOnly]

class AdminRetrieveUpdateDestroyAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Admin.objects.all()
    serializer_class = AdminSerializer
    permission_classes = [IsAuthenticatedAndAdminOrReadOnly]

class CategoryListCreateAPIView(generics.ListCreateAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer

class CategoryRetrieveUpdateDestroyAPIView(ModelRetrieveUpdateDestroyAPIView):
    serializer_class = CategorySerializer
    queryset = Category.objects.all()

class CustomerListCreateAPIView(generics.ListCreateAPIView):
    queryset = Customer.objects.all()
    serializer_class = CustomerSerializer

class CustomerRetrieveUpdateDestroyAPIView(ModelRetrieveUpdateDestroyAPIView):
    serializer_class = CustomerSerializer
    queryset = Customer.objects.all()

class ProductListCreateAPIView(ModelListCreateAPIView):
    serializer_class = ProductSerializer
    queryset = Product.objects.all()

class ProductRetrieveUpdateDestroyAPIView(ModelRetrieveUpdateDestroyAPIView):
    serializer_class = ProductSerializer
    queryset = Product.objects.all()

class ItemsListCreateAPIView(generics.ListCreateAPIView):
    queryset = Item.objects.all()
    serializer_class = ItemSerializer

class ItemsRetrieveUpdateDestroyAPIView(ModelRetrieveUpdateDestroyAPIView):
    serializer_class = ItemSerializer
    queryset = Item.objects.all()

class ShopCardListCreateAPIView(generics.ListCreateAPIView):
    queryset = ShopCard.objects.all()
    serializer_class = ShopCardSerializer
    permission_classes = [IsAuthenticatedAndAdminOrReadOnly]

class ShopCardRetrieveUpdateDestroyAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = ShopCard.objects.all()
    serializer_class = ShopCardSerializer
    permission_classes = [IsAuthenticatedAndAdminOrReadOnly]

@api_view(['POST'])
def add_to_cart(request):
    customer_id = request.data.get('customer_id')
    product_id = request.data.get('product_id')
    quantity = request.data.get('quantity')

    customer = get_object_or_404(Customer, pk=customer_id)
    product = get_object_or_404(Product, pk=product_id)

    try:
        quantity = int(quantity)
        if quantity <= 0:
            raise ValueError("Quantity must be a positive integer")
    except (TypeError, ValueError):
        return Response({'error': 'Invalid quantity'}, status=status.HTTP_400_BAD_REQUEST)

    shop_cart, created = ShopCard.objects.get_or_create(customer=customer)
    Item.objects.create(product=product, quantity=quantity, shop_card=shop_cart)
    
    return Response({'message': 'Item added to cart successfully'}, status=status.HTTP_200_OK)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def purchase_history(request, customer_id):
    purchases = Purchase.objects.filter(customer_id=customer_id)
    serializer = PurchaseSerializer(purchases, many=True)
    return Response(serializer.data)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def check_total_purchase(request, customer_id):
    total_purchase = Purchase.objects.filter(customer_id=customer_id).aggregate(Sum('quantity'))['quantity__sum']
    if total_purchase and total_purchase > 10000:
        return Response({'message': 'Total purchase exceeds $10000'}, status=status.HTTP_200_OK)
    else:
        return Response({'message': 'Total purchase does not exceed $10000'}, status=status.HTTP_400_BAD_REQUEST)


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
            return Response({'message': 'Total purchase exceeds $10000'}, status=status.HTTP_200_OK)
        else:
            return Response({'message': 'Total purchase does not exceed $10000'}, status=status.HTTP_400_BAD_REQUEST)
        
class TotalProducts(APIView):
    def get(self, request):
        total_products = Product.objects.count()
        return Response({'total_products': total_products}, status=status.HTTP_200_OK)
    
class ExpiredProducts(APIView):
    def get(self, request):
        threshold_date = timezone.now() - timezone.timedelta(days=30)
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
       
class PurchaseView(APIView):
    def post(self, request):
        customer_id = int(request.data.get('customer_id'))  # Convert to integer
        product_id = int(request.data.get('product_id'))    # Convert to integer
        quantity = int(request.data.get('quantity'))        # Convert to integer

        try:
            customer = Customer.objects.get(pk=customer_id)
            product = Product.objects.get(pk=product_id)
        except (Customer.DoesNotExist, Product.DoesNotExist):
            return Response({'error': 'Customer or product not found'}, status=status.HTTP_404_NOT_FOUND)

        if quantity <= 0:
            return Response({'error': 'Invalid quantity'}, status=status.HTTP_400_BAD_REQUEST)

        if customer.make_purchase(product, quantity):
            Purchase.objects.create(customer=customer, product=product, quantity=quantity)
            return Response({'message': 'Purchase successful'}, status=status.HTTP_201_CREATED)
        else:
            return Response({'error': 'Insufficient balance or quantity not available'}, status=status.HTTP_400_BAD_REQUEST)     
        
def home(request):
    return render(request, 'index.html', {})

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def purchase_history(request, customer_id):
    purchases = Purchase.objects.filter(customer_id=customer_id)
    serializer = PurchaseSerializer(purchases, many=True)
    return Response(serializer.data)

@api_view(['GET'])
class CheckTotalPurchase(APIView):
    def get(self, request, customer_id):
        total_purchase = Purchase.objects.filter(customer_id=customer_id).aggregate(Sum('quantity'))['quantity__sum']
        if total_purchase and total_purchase > 10000:
            return Response({'message': 'Total purchase exceeds $10000'}, status=status.HTTP_200_OK)
        else:
            return Response({'message': 'Total purchase does not exceed $10000'}, status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def make_purchase(request):
    customer_id = request.data.get('customer_id')
    product_id = request.data.get('product_id')
    quantity = request.data.get('quantity')

    customer = get_object_or_404(Customer, pk=customer_id)
    product = get_object_or_404(Product, pk=product_id)

    if quantity <= 0:
        return Response({'error': 'Invalid quantity'}, status=status.HTTP_400_BAD_REQUEST)

    if customer.make_purchase(product, quantity):
        Purchase.objects.create(customer=customer, product=product, quantity=quantity)
        return Response({'message': 'Purchase successful'}, status=status.HTTP_201_CREATED)
    else:
        return Response({'error': 'Insufficient balance or quantity not available'}, status=status.HTTP_400_BAD_REQUEST)

class PurchaseHistoryAPIView(generics.ListAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = PurchaseSerializer

    def get_queryset(self):
        customer_id = self.kwargs['customer_id']
        return Purchase.objects.filter(customer_id=customer_id)
    
    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)
     
class CheckTotalPurchase(APIView):
    def get(self, request, customer_id):
        total_purchase = Purchase.objects.filter(customer_id=customer_id).aggregate(Sum('quantity'))['quantity__sum']
        if total_purchase and total_purchase > 1000000:
            return Response({'message': 'Total purchase exceeds $10000'}, status=status.HTTP_200_OK)
        else:
            return Response({'message': 'Total purchase does not exceed $10000'}, status=status.HTTP_400_BAD_REQUEST)
        
class TotalProducts(APIView):
    def get(self, request):
        total_products = Product.objects.count()
        return Response({'total_products': total_products}, status=status.HTTP_200_OK)
    
class ExpiredProducts(APIView):
    def get(self, request):
        threshold_date = timezone.now() - timezone.timedelta(days=30)
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
       
class PurchaseView(APIView):
    def post(self, request):
        customer_id = int(request.data.get('customer_id'))  # Convert to integer
        product_id = int(request.data.get('product_id'))    # Convert to integer
        quantity = int(request.data.get('quantity'))        # Convert to integer

        try:
            customer = Customer.objects.get(pk=customer_id)
            product = Product.objects.get(pk=product_id)
        except (Customer.DoesNotExist, Product.DoesNotExist):
            return Response({'error': 'Customer or product not found'}, status=status.HTTP_404_NOT_FOUND)

        if quantity <= 0:
            return Response({'error': 'Invalid quantity'}, status=status.HTTP_400_BAD_REQUEST)

        if customer.make_purchase(product, quantity):
            Purchase.objects.create(customer=customer, product=product, quantity=quantity)
            return Response({'message': 'Purchase successful'}, status=status.HTTP_201_CREATED)
        else:
            return Response({'error': 'Insufficient balance or quantity not available'}, status=status.HTTP_400_BAD_REQUEST)
      