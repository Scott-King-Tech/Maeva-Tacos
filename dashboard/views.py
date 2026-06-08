from django.shortcuts import render,get_object_or_404,redirect
from django.contrib.auth.decorators import login_required
from orders.models import Order
from django.http import JsonResponse

# Create your views here.

def home(request):
        return render(request, 'home.html')

@login_required
def producer_dashboard(request):
    if request.user.role != 'producer':
        return redirect(home)  # Redirect non-producers to home or another appropriate page

    new_orders = Order.objects.filter(status='placed').order_by('-created_at')
    confirmed_orders = Order.objects.filter(status='confirmed').order_by('-created_at')
    cooking_orders = Order.objects.filter(status='cooking').order_by('-created_at')
    ready_orders = Order.objects.filter(status='ready').order_by('-created_at')
    context = {
        'new_orders': new_orders,
        'confirmed_orders': confirmed_orders,
        'cooking_orders': cooking_orders,
        'ready_orders': ready_orders,
    }
    return render(request, 'dashboard/producer_dashboard.html', context)

@login_required
def update_order_status(request, order_id):
    if request.user.role != 'producer':
        return JsonResponse({'error': 'Unauthorized'}, status=403)

    if request.method != 'POST':
        return JsonResponse({'error': 'POST request required'}, status=405)

    order = get_object_or_404(Order, id=order_id)
    new_status = request.POST.get('status')

    valid_transitions = {
        'placed': ['confirmed'],
        'confirmed': ['cooking'],
        'cooking': ['ready'],
        'ready': ['completed'],
    }

    if new_status in valid_transitions.get(order.status, []):
        order.status = new_status
        order.save()
        return JsonResponse({'success': True, 'new_status': order.status})
    
    return JsonResponse({'error': 'Invalid status transition'}, status=400)