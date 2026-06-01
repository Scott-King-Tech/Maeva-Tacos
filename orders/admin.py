from django.contrib import admin
from .models import Taco, Order, OrderItem


@admin.register(Taco)
class TacoAdmin(admin.ModelAdmin):
    list_display = ['name', 'price', 'is_spicy']


class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 1


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ['id', 'customer', 'status', 'total_price', 'created_at']
    list_filter = ['status', 'created_at']
    inlines = [OrderItemInline]