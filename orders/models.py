from django.db import models
from users.models import User


class Taco(models.Model):
    name = models.CharField(max_length=100)
    price = models.DecimalField(max_digits=6, decimal_places=2)
    is_spicy = models.BooleanField(default=False)
    description = models.TextField(blank=True)
    images = models.ImageField(upload_to='taco_images/', blank=True, null=True)
    
    def __str__(self):
        return self.name


class Order(models.Model):
    STATUS_CHOICES = [
        ('placed', 'Placed'),
        ('confirmed', 'Confirmed'),
        ('cooking', 'Cooking'),
        ('ready', 'Ready'),
        ('completed', 'Completed'),
        ('cancelled', 'Cancelled'),
    ]
    
    customer = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='orders'
    )
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='placed'
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    @property
    def total_price(self):
        return sum(item.subtotal for item in self.items.all())
    
    def __str__(self):
        return f"Order #{self.id} - {self.status}"


class OrderItem(models.Model):
    order = models.ForeignKey(
        Order,
        on_delete=models.CASCADE,
        related_name='items'
    )
    taco = models.ForeignKey(Taco, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    unit_price = models.DecimalField(max_digits=6, decimal_places=2)
    
    @property
    def subtotal(self):
        return self.quantity * self.unit_price
    
    def __str__(self):
        return f"{self.quantity}x {self.taco.name}"