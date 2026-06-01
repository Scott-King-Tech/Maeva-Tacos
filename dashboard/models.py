from django.db import models
from users.models import User
# Create your models here.


class Expense(models.Model):
    CATEGORY_CHOICES = [
        ('ingredients', 'Ingredients'),
        ('utilities', 'Utilities'),
        ('packaging', 'Packaging'),
        ('other', 'Other'),
    ]
    producer = models.ForeignKey(User,on_delete=models.CASCADE,related_name='expenses')
    name = models.CharField(max_length=100)
    category = models.CharField(max_length=20,choices=CATEGORY_CHOICES)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    date = models.DateField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.name} - ${self.amount}"