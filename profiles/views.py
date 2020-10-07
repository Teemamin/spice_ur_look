from django.shortcuts import render, get_object_or_404
from django.contrib import messages


from .models import UserProfile
from .forms import UserProfileForm
from checkout.models import Order


# Create your views here.


def profile_view(request):
    profile = get_object_or_404(UserProfile, user=request.user)
    if request.method == 'POST':
        form = UserProfileForm(request.POST, instance=profile)
        if form.is_valid():
            form.save()
            messages.success(request, 'Updated your Profile successfully!')
        else:
            messages.error(request, 'Update failed. Kindly check\
                that your inputs are valid.')
    else:
        form = UserProfileForm(instance=profile)

    profile_orders = profile.orders.all()

    context = {
        'form': form,
        'profile_orders': profile_orders,
        'on_profile_page': True
    }
    return render(request, 'profiles/profile.html', context)



def order_history_view(request, order_number):
    order = get_object_or_404(Order, order_number=order_number)

    messages.info(request, (
        f'This is a previous order confirmation on order number {order_number}\
          An email was sent for the said order. '
        
    ))

    template = 'checkout/checkout_success.html'
    context = {
        'order': order,
        'from_profile': True,
    }

    return render(request, template, context)


