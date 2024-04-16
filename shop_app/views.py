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

@api_view(['GET', 'POST'])
@permission_classes([AllowAny])
def user_login(request):
    if request.method == 'POST':
        username = request.data.get('username')
        password = request.data.get('password')

        if not username or not password:
            return JsonResponse({'error': 'Username and password are required'}, status=400)

        user = authenticate(username=username, password=password)

        if user is None:
            return JsonResponse({'error': 'Invalid credentials'}, status=401)

        login(request, user)
        return redirect('/')  # Redirect to the home page

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

        login(request, user)
        return redirect('/')
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
        return JsonResponse({'error': 'Profile does not exist'}, status=404)

def user_logout(request):
    logout(request)
    return redirect('home')

# @api_view(['POST'])
# @permission_classes([IsAuthenticated])
# def add_to_cart(request):
#     customer = request.user.customer
#     products = request.data.get('products', [])  # Assuming products are sent in the request data

#     items = []
#     for product_data in products:
#         product_id = product_data.get('id')
#         quantity = product_data.get('quantity', 1)  # Default quantity is 1 if not specified

#         try:
#             product = Product.objects.get(pk=product_id)
#         except Product.DoesNotExist:
#             return Response({'error': f'Product with id {product_id} does not exist'}, status=status.HTTP_404_NOT_FOUND)

#         # Create or update the item in the cart
#         item, created = Item.objects.get_or_create(customer=customer, product=product, purchase=None)
#         if not created:
#             item.quantity += quantity
#             item.save()

#         items.append(item)

#     serializer = ItemSerializer(items, many=True)
#     return Response(serializer.data, status=status.HTTP_201_CREATED)

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
        products_with_sales = Product.objects.annotate(total_sales=Count('purchase__id'))
        products_ordered = products_with_sales.order_by('-total_sales')

        if not products_ordered.exists():
            return Response({'message': 'No products found'}, status=status.HTTP_404_NOT_FOUND)

        wb = openpyxl.Workbook()
        ws = wb.active

        ws.append(['Name', 'Price', 'Quantity', 'Total Sales'])

        for product in products_ordered:
            ws.append([product.name, product.price, product.quantity, product.total_sales])

        from io import BytesIO
        excel_file = BytesIO()
        wb.save(excel_file)
        excel_file.seek(0)

        response = HttpResponse(excel_file, content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
        response['Content-Disposition'] = 'attachment; filename=products.xlsx'

        return response
        
# @api_view(['GET','POST'])  
# @permission_classes([IsAuthenticated])
@csrf_exempt
def make_purchase(request):
    if request.method == 'POST':
        customer_id = request.POST.get('customer_id')
        product_id = request.POST.get('product_id')
        quantity = request.POST.get('quantity')

        try:
            customer = Customer.objects.get(id=customer_id)
            product = Product.objects.get(id=product_id)
        except (Customer.DoesNotExist, Product.DoesNotExist):
            return JsonResponse({'error': 'Customer or product not found'}, status=404)

        try:
            quantity = int(quantity)
            if quantity <= 0:
                raise ValueError("Quantity must be a positive integer")
        except ValueError:
            return JsonResponse({'error': 'Invalid quantity'}, status=400)

        if customer.balance < product.price * quantity:
            return JsonResponse({'error': 'Insufficient balance'}, status=400)

        try:
            Purchase.objects.create(customer=customer, product=product, quantity=quantity)
            customer.balance -= product.price * quantity
            customer.save()
            return JsonResponse({'message': 'Purchase successful'}, status=201)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=400)

    customers = Customer.objects.all()
    products = Product.objects.all()
    return render(request, 'purchase.html', {'customers': customers, 'products': products})

class PurchaseHistoryAPIView(generics.ListAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = PurchaseSerializer

    def get_queryset(self):
        customer_id = self.kwargs['customer_id']
        return Purchase.objects.filter(customer_id=customer_id)
    
    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)

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

class CheckTotalPurchase(APIView):
    def get(self, request, customer_id):
        total_purchase = Purchase.objects.filter(customer_id=customer_id).aggregate(Sum('quantity'))['quantity__sum']
        if total_purchase and total_purchase > 10000:
            return Response({'message': 'Total purchase exceeds $10000'}, status=status.HTTP_200_OK)
        else:
            return Response({'message': 'Total purchase does not exceed $10000'}, status=status.HTTP_400_BAD_REQUEST)
        
def purchase_page(request):
    customers = Customer.objects.all()
    products = Product.objects.all()
    return render(request, 'buy.html', {'customers': customers, 'products': products})

