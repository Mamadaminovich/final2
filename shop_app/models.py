from django.db import models
from django.db import transaction
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import User

class Admin(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    
    def __str__(self) -> str:
        return self.name

class Category(models.Model):
    name = models.CharField(max_length=100)
    
    def __str__(self) -> str:
        return self.name

class Customer(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()
    balance = models.DecimalField(max_digits=10, decimal_places=2, default=0)

    def make_purchase(self, product, quantity):
        total_cost = product.price * quantity
        if self.balance >= total_cost:
            self.balance -= total_cost
            self.save()
            product.update_quantity(quantity)
            return True
        else:
            return "Not enough balance to make the purchase."

class Product(models.Model):
    name = models.CharField(max_length=100)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    quantity = models.IntegerField()
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    
    def update_quantity(self, quantity):
        self.quantity -= quantity
        self.save()
        if self.quantity <= 0:
            self.delete()
            
class Purchase(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.IntegerField()
    purchase_date = models.DateTimeField(auto_now_add=True)

    @staticmethod
    def make_purchase(customer, product, quantity):
        if customer.make_purchase(product, quantity):
            Purchase.objects.create(customer=customer, product=product, quantity=quantity)
            return True
        else:
            return False

class ShopCard(models.Model):
    customer = models.OneToOneField(Customer, on_delete=models.CASCADE, related_name='shop_card')
    created_at = models.DateTimeField(auto_now_add=True)
        
    def __str__(self) -> str:
        return str(self.customer)
    
class Item(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE, related_name='items')
    purchase = models.ForeignKey(Purchase, on_delete=models.CASCADE, related_name='items')
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)

    def __str__(self):
        return f"{self.quantity} of {self.product.name} in {self.purchase}"
    
class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    hobbies = models.CharField(max_length=100, blank=True)
    birth_year = models.IntegerField(null=True, blank=True)
    receive_ads = models.BooleanField(default=False)

    def __str__(self):
        return self.user.username
    
@receiver(post_save, sender=Purchase)
def update_product_quantity(sender, instance, created, **kwargs):
    if created:
        with transaction.atomic():
            instance.product.update_quantity(instance.quantity)
            
@receiver(post_save, sender=Item)
def update_shop_card_balance(sender, instance, created, **kwargs):
    if created:
        with transaction.atomic():
            total_cost = instance.product.price * instance.quantity
            instance.shop_card.customer.balance -= total_cost
            instance.shop_card.customer.save()
            