from django.contrib import admin
from .models import *
admin.site.site_header = 'Shop Store Admin Panel'
admin.site.site_title = 'Shop Store'

@admin.register(Admin)
class MyAdmin(admin.ModelAdmin):
    list_display = ('name',) 
    search_fields = ('name', 'email')

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name',) 
    search_fields = ('name',)

@admin.register(Customer)
class CustomerAdmin(admin.ModelAdmin):
    list_display = ('name', 'email') 
    search_fields = ('name', 'email')

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'price', 'get_category') 
    search_fields = ('name', 'category__name') 
    list_filter = ('category',)

    def get_category(self, obj):
        return obj.category.name 

    get_category.short_description = 'Category'

@admin.register(Purchase)
class PurchaseAdmin(admin.ModelAdmin):
    list_display = ('customer', 'product', 'quantity', 'purchase_date') 
    search_fields = ('customer__name', 'product__name')
    list_filter = ('customer', 'product')
    
@admin.register(Basket)
class BasketAdmin(admin.ModelAdmin):
    list_display = ('user',)
    search_fields = ('user__username',)

@admin.register(BasketItem)
class BasketItemAdmin(admin.ModelAdmin):
    list_display = ('basket', 'product', 'quantity') 
    search_fields = ('basket__user__username', 'product__name')
    list_filter = ('basket__user',)
    
@admin.register(Item)
class ItemAdmin(admin.ModelAdmin):
    list_display = ('product', 'quantity', 'shop_card') 
    search_fields = ('product__name', 'shop_card__customer__name')
    list_filter = ('shop_card__customer',)

@admin.register(ShopCard)
class ShopCardAdmin(admin.ModelAdmin):
    list_display = ('customer', 'created_at') 
    search_fields = ('customer__name',)
    list_filter = ('customer',)
    
admin.site.register(Profile)


    
