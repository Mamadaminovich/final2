from django.contrib import admin
from .models import *

admin.site.site_header = 'Shop Store Admin Panel'
admin.site.site_title = 'Shop Store'

@admin.register(AdminUser)
class AdminUserAdmin(admin.ModelAdmin):
    list_display = ('user',) 
    search_fields = ('user__username', 'user__email')

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name',) 
    search_fields = ('name',)

@admin.register(Customer)
class CustomerAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'balance') 
    search_fields = ('name', 'email')

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'price', 'quantity', 'category') 
    search_fields = ('name', 'category__name') 
    list_filter = ('category',)

@admin.register(Purchase)
class PurchaseAdmin(admin.ModelAdmin):
    list_display = ('customer', 'product', 'quantity', 'purchase_date') 
    search_fields = ('customer__name', 'product__name')
    list_filter = ('customer', 'product')

@admin.register(Basket)
class BasketAdmin(admin.ModelAdmin):
    list_display = ('customer', 'created_at') 
    search_fields = ('customer__name',)
    list_filter = ('customer',)

@admin.register(BasketItem)
class BasketItemAdmin(admin.ModelAdmin):
    list_display = ('basket', 'product', 'quantity') 
    search_fields = ('basket__customer__name', 'product__name')
    list_filter = ('basket', 'product')

@admin.register(ShopCart)
class ShopCartAdmin(admin.ModelAdmin):
    list_display = ('customer', 'created_at') 
    search_fields = ('customer__name',)
    list_filter = ('customer',)
    
@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'hobbies', 'birth_year', 'receive_ads') 
    search_fields = ('user__username',)
    list_filter = ('receive_ads',)