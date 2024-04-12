from django.urls import path, include
from rest_framework import routers
from .views import *

router = routers.DefaultRouter()

urlpatterns = [
    path('', home, name='home'),
    path('admins/', AdminListCreateAPIView.as_view(), name='admin-list-create'),
    path('admins/<int:pk>/', AdminRetrieveUpdateDestroyAPIView.as_view(), name='admin-retrieve-update-destroy'),
    path('categories/', CategoryListCreateAPIView.as_view(), name='category-list-create'),  # Corrected pattern name
    path('categories/<int:pk>/', CategoryRetrieveUpdateDestroyAPIView.as_view(), name='category-retrieve-update-destroy'),
    path('customers/', CustomerListCreateAPIView.as_view(), name='customer-list-create'),
    path('customers/<int:pk>/', CustomerRetrieveUpdateDestroyAPIView.as_view(), name='customer-retrieve-update-destroy'),
    path('products/', ProductListCreateAPIView.as_view(), name='product-list-create'),
    path('products/<int:pk>/', ProductRetrieveUpdateDestroyAPIView.as_view(), name='product-retrieve-update-destroy'),
    path('purchases/', PurchaseView.as_view(), name='purchase-create'),
    path('purchases/customer/<int:customer_id>/', PurchaseHistoryAPIView.as_view(), name='purchase-history'),
    path('shopcards/', ShopCardListCreateAPIView.as_view(), name='shopcard-list-create'),  # Corrected pattern name
    path('shopcards/<int:pk>/', ShopCardRetrieveUpdateDestroyAPIView.as_view(), name='shopcard-retrieve-update-destroy'),  # Corrected pattern name
    path('items/', ItemsListCreateAPIView.as_view(), name='item-list-create'),
    path('items/<int:pk>/', ItemsRetrieveUpdateDestroyAPIView.as_view(), name='item-retrieve-update-destroy'),  
    path('check-total-purchase/<int:customer_id>/', CheckTotalPurchase.as_view(), name='check-total-purchase'),
    path('total-products/', TotalProducts.as_view(), name='total-products'),
    path('expired-products/', ExpiredProducts.as_view(), name='expired-products'),
    path('most-sold-product/', MostSoldProduct.as_view(), name='most-sold-product'),
    path('optional-user-request/', OptionalUserRequest.as_view(), name='optional-user-request'),
]