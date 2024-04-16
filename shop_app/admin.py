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

@admin.register(ShopCard)
class ShopCardAdmin(admin.ModelAdmin):
    list_display = ('customer', 'created_at') 
    search_fields = ('customer__name',)
    list_filter = ('customer',)
    
admin.site.register(Profile)
admin.site.register(Item)

    
