from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, get_object_or_404
from django.views import View
from django.shortcuts import render
from .forms import UserRegistration, OrderCreationForm, AIFormSet
from .models import Order, User


class Registration(View):
    template_name = 'registration/registration.html'

    def get(self, request):
        context = {
            'form': UserRegistration()
        }
        return render(request, self.template_name, context)

    def post(self, request):
        form = UserRegistration(request.POST, request.FILES)

        if form.is_valid():
            form.save()
            return redirect('login')

        context = {
            'form': form
        }

        return render(request, self.template_name, context)


def user_orders_count(request):
    num_orders = Order.objects.count()

    return render(request, 'user/user_account.html', context={
        'num_orders': num_orders,
    })


class OrderCreate(View):
    template_name = 'user/order_create_user.html'

    def get(self, request):
        context = {
            'form': OrderCreationForm()
        }
        return render(request, self.template_name, context)

    def post(self, request):
        form = OrderCreationForm(request.POST, request.FILES)

        if form.is_valid():
            form.save()
            return redirect('login')

        context = {
            'form': form
        }

        return render(request, self.template_name, context)



@login_required
def profile_delete(request, pk):
    order = get_object_or_404(Order, pk=pk)
    if not request.user.is_author(order):
        return redirect('my-account')
    if request.method == 'POST':
        order.delete()
        return redirect('my-account')
    else:
        context = {'order': order}
        return render(request, 'home', context)
