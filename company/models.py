from django.db import models
from django.contrib.auth.hashers import check_password ,make_password

from logp.models import RegistrationForm



class Company(models.Model):
    company_id = models.CharField(primary_key=True, max_length=6, null=False, unique=True)
    company_name = models.CharField(max_length=255)
    contact_email = models.EmailField()
    password = models.CharField(max_length=255)  
    
    def __str__(self):
        return self.company_id
    
    def save(self, *args, **kwargs):
        if not self.password.startswith('pbkdf2_sha256$'):  # Avoid double hashing
            self.password = make_password(self.password)
        super().save(*args, **kwargs)

    def check_password(self, raw_password):
        return self.password == raw_password


class Vehicle(models.Model):
    Vehicle_id = models.CharField(primary_key=True,max_length=6,null=False)
    company= models.ForeignKey(Company,on_delete=models.CASCADE)
    company_name = models.CharField(max_length=255)
    Vehicle_name = models.CharField(max_length=255,null=True)
    Wheel = models.CharField(max_length=5,null=True)
    Year = models.CharField(max_length=4)
    Fuel = models.CharField(max_length=10)
    Type = models.CharField(max_length=25)
    image=models.ImageField(upload_to="img")
    def __str__(self):
        return self.Vehicle_id
    
    
class SPARE(models.Model):
    spare_id = models.CharField(primary_key=True, max_length=6, null=False)
    vehicle = models.ForeignKey(Vehicle, on_delete=models.CASCADE)
    company = models.ForeignKey(Company, on_delete=models.CASCADE)
    spare_name = models.CharField(max_length=255)
    typ = models.CharField(max_length=255,null=True, blank=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    description = models.TextField(null=True, blank=True)
    image=models.ImageField(upload_to="img",null=True, blank=True)
    stock = models.PositiveIntegerField(null=True, blank=True)

    def __str__(self):
        return self.spare_name
    
class Order(models.Model):
    order_id = models.AutoField(primary_key=True)
    user = models.ForeignKey(RegistrationForm, on_delete=models.CASCADE, blank=True, null=True)
    product = models.ForeignKey(SPARE, on_delete=models.CASCADE)
    total_price = models.DecimalField(max_digits=10, decimal_places=2)
    is_paid = models.BooleanField(default=False)
    payment_id = models.CharField(max_length=100, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    payment_method = models.CharField(
        max_length=10,
        choices=[("COD", "Cash on Delivery"), ("ONLINE", "Online Payment")],
        default="ONLINE"
    )  

    status = models.CharField(
        max_length=20,
        choices=[("Pending", "Pending"), ("Completed", "Completed"), ("Cancelled", "Cancelled")],
        default="Pending"
    )

    def __str__(self):
        return f"Order {self.order_id} - {self.get_payment_method_display()}"
    
    
class Cart(models.Model):
    cart_id = models.AutoField(primary_key=True)
    spare = models.ForeignKey(SPARE, on_delete=models.CASCADE, related_name="cart_items")
    user = models.ForeignKey(RegistrationForm, on_delete=models.CASCADE, related_name="cart_items")
    fname = models.CharField(max_length=50)
    email = models.EmailField()

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Cart {self.cart_id} - {self.spare.spare_name} by {self.email}"
    
    
class ProductRating(models.Model):
    user = models.ForeignKey(RegistrationForm, on_delete=models.CASCADE)
    product = models.ForeignKey(SPARE, on_delete=models.CASCADE)
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    rating = models.PositiveIntegerField()  # 1 to 5 stars
    review = models.TextField(blank=True, null=True)
    rated_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'product', 'order')  # Prevent duplicate ratings per order

    def __str__(self):
        return f"{self.user.email} rated {self.product.spare_name} - {self.rating}★"
