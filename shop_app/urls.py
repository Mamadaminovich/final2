from django.urls import path, include
from rest_framework import routers
from .views import *

router = routers.DefaultRouter()

urlpatterns = [
    path('', home, name='home'),
    path('admins/', AdminListCreateAPIView.as_view(), name='admin-list-create'),
    path('admins/<int:pk>/', AdminRetrieveUpdateDestroyAPIView.as_view(), name='admin-retrieve-update-destroy'),
    path('categories/', CategoryListCreateAPIView.as_view(), name='category-list-create'),
    path('categories/<int:pk>/', CategoryRetrieveUpdateDestroyAPIView.as_view(), name='category-retrieve-update-destroy'),
    path('customers/', CustomerListCreateAPIView.as_view(), name='customer-list-create'),
    path('customers/<int:pk>/', CustomerRetrieveUpdateDestroyAPIView.as_view(), name='customer-retrieve-update-destroy'),
    path('products/', ProductListCreateAPIView.as_view(), name='product-list-create'),
    path('products/<int:pk>/', ProductRetrieveUpdateDestroyAPIView.as_view(), name='product-retrieve-update-destroy'),
    path('purchase/', PurchaseView.as_view(), name='purchase-create'),
    path('purchase-page/', purchase_page, name='purchase_page'),
    path('add-to-cart/', add_to_cart, name='add_to_cart'),
    path('purchase-history', purchase_history, name='purchase_history'),
    path('purchase/customer/<int:customer_id>/', PurchaseHistoryAPIView.as_view(), name='purchase-history'),
    path('shopcards/', ShopCardListCreateAPIView.as_view(), name='shopcard-list-create'),
    path('shopcards/<int:pk>/', ShopCardRetrieveUpdateDestroyAPIView.as_view(), name='shopcard-retrieve-update-destroy'),
    path('items/', ItemsListCreateAPIView.as_view(), name='item-list-create'),
    path('items/<int:pk>/', ItemsRetrieveUpdateDestroyAPIView.as_view(), name='item-retrieve-update-destroy'),
    path('check-total-purchase/<int:customer_id>/', CheckTotalPurchase.as_view(), name='check-total-purchase'),
    path('total-products/', TotalProducts.as_view(), name='total-products'),
    path('expired-products/', ExpiredProducts.as_view(), name='expired-products'),
    path('make-purchase/', make_purchase, name='make_purchase'),
    path('most-sold-product/', MostSoldProduct.as_view(), name='most-sold-product'),
    path('register/', register, name='register'),
    path('user-login/', user_login, name='user_login'),
    path('logout/', user_logout, name='logout'),
    path('update-ads-preference/', update_receive_ads_preference, name='update_ads_preference'),
]