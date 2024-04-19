from django.shortcuts import render, redirect
from .models import *
from .serializers import *
from django.db.models import Sum, Count
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework.exceptions import ValidationError
from .permissions import IsAuthenticatedAndAdminOrReadOnly
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponseRedirect, JsonResponse, HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.utils import timezone
from rest_framework.permissions import IsAuthenticated, AllowAny, IsAuthenticatedOrReadOnly
from rest_framework import generics, status
from django.views.decorators.csrf import csrf_exempt
import openpyxl

def home(request):
    return render(request, 'index.html', {})

class ModelListCreateAPIView(generics.ListCreateAPIView):
    permission_classes = [IsAuthenticatedAndAdminOrReadOnly]
    serializer_class = None
    queryset = None

class ModelRetrieveUpdateDestroyAPIView(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [IsAuthenticatedAndAdminOrReadOnly]
    serializer_class = None
    queryset = None

class AdminListCreateAPIView(generics.ListCreateAPIView):
    queryset = AdminUser.objects.all()
    serializer_class = AdminSerializer
    permission_classes = [IsAuthenticatedAndAdminOrReadOnly]

class AdminRetrieveUpdateDestroyAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = AdminUser.objects.all()
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
    queryset = BasketItem.objects.all()
    serializer_class = ItemSerializer

class ItemsRetrieveUpdateDestroyAPIView(ModelRetrieveUpdateDestroyAPIView):
    serializer_class = ItemSerializer
    queryset = BasketItem.objects.all()

class ShopCardListCreateAPIView(generics.ListCreateAPIView):
    queryset = ShopCart.objects.all()
    serializer_class = ShopCardSerializer
    permission_classes = [IsAuthenticatedAndAdminOrReadOnly]

class ShopCardRetrieveUpdateDestroyAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = ShopCart.objects.all()
    serializer_class = ShopCardSerializer
    permission_classes = [IsAuthenticatedAndAdminOrReadOnly]
    

@api_view(['GET', 'POST'])
@permission_classes([AllowAny])
def user_login(request):
    if request.method == 'POST':
        username = request.data.get('username')
        password = request.data.get('password')

        if not username or not password:
            return Response({'error': 'Username and password are required'}, status=status.HTTP_400_BAD_REQUEST)

        user = authenticate(username=username, password=password)

        if user is None:
            return Response({'error': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)

        login(request, user)
        return redirect('home') 

    return render(request, 'login.html')

@api_view(['GET', 'POST'])
@permission_classes([AllowAny])
def register(request):
    if request.method == 'POST':
        username = request.data.get('username')
        password = request.data.get('password')
        email = request.data.get('email')
        hobbies = request.data.get('hobbies')
        birth_year = request.data.get('birth_year')
        receive_ads = request.data.get('receive_ads', False)

        if not username or not password or not email:
            return JsonResponse({'error': 'Username, password, and email are required'}, status=400)

        if User.objects.filter(username=username).exists():
            return JsonResponse({'error': 'Username already exists'}, status=400)

        user = User.objects.create_user(username=username, password=password, email=email)
        profile = Profile.objects.create(user=user, hobbies=hobbies, birth_year=birth_year, receive_ads=receive_ads)

        return redirect('user_login')
    else:
        return render(request, 'register.html')

@api_view(['PATCH'])
def update_receive_ads_preference(request):
    user = request.user
    receive_ads = request.data.get('receive_ads', False)

    if user.is_anonymous:
        return JsonResponse({'error': 'User not authenticated'}, status=401)

    try:
        profile = user.profile
        profile.receive_ads = receive_ads
        profile.save()
        return JsonResponse({'message': 'Receive ads preference updated successfully'}, status=200)
    except Profile.DoesNotExist:
        return Response({'error': 'Profile does not exist'}, status=status.HTTP_404_NOT_FOUND)

def user_logout(request):
    logout(request)
    return redirect('home')

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
        return Response({'message': ' HUUH Total purchase exceeds $10000!!!!!!'}, status=status.HTTP_200_OK)
    else:
        return Response({'message': 'Total purchase does not exceed $10000'}, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET','POST'])       
def purchase_page(request):
    return render(request, 'a.html')

@api_view(['GET','POST'])  
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



@api_view(['POST'])
def add_to_basket(request):
    product_id = request.data.get('product_id')
    quantity = request.data.get('quantity')
    if not product_id or not quantity:
        return Response({"error": "Product ID and quantity are required."}, status=status.HTTP_400_BAD_REQUEST)
    
    try:
        product = Product.objects.get(id=product_id)
        if product.quantity < quantity:
            return Response({"error": "Not enough quantity available."}, status=status.HTTP_400_BAD_REQUEST)
        
        # Add the product to the basket
        product.in_basket = True
        product.save()
        
        # Add the item to the shopping cart
        shop_card = request.user.customer.shop_card
        Item.objects.create(product=product, quantity=quantity, shop_card=shop_card, in_basket=True)
        
        return Response({"success": "Product added to basket successfully."}, status=status.HTTP_201_CREATED)
    except Product.DoesNotExist:
        return Response({"error": "Product not found."}, status=status.HTTP_404_NOT_FOUND)

@api_view(['POST'])
def remove_from_basket(request):
    item_id = request.data.get('item_id')
    if not item_id:
        return Response({"error": "Item ID is required."}, status=status.HTTP_400_BAD_REQUEST)
    try:
        item = Item.objects.get(id=item_id)
        item.in_basket = False
        item.product.in_basket = False
        item.save()
        item.product.save()
        return Response({"success": "Product removed from basket successfully."}, status=status.HTTP_204_NO_CONTENT)
    except Item.DoesNotExist:
        return Response({"error": "Item not found."}, status=status.HTTP_404_NOT_FOUND)
