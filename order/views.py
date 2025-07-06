from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import get_object_or_404, render, redirect
from django.views import View
from appuser.mixin import CustomerRequiredMixin
from cart.models import Cart, CartItem
from iran.models import Province
from order.forms import ExtraOrderInfoForm, OrderAddressForm
from order.models import Order, OrderItems
from asgiref.sync import async_to_sync
from Utility.VerificationMessageSender import VerificationMessageSender, SmsSender


class PlaceOrderView(LoginRequiredMixin, CustomerRequiredMixin, View):

    def create_order(self,total_amount,cart_items):
        order = Order.objects.create(user=self.request.user)

        for item in cart_items:
            OrderItems.objects.create(
                order=order,
                product=item.product,
                price=item.price,
                quantity=item.quantity
            )
            item.delete()
        order.total_amount = total_amount
        order.province = self.request.user.province
        order.district = self.request.user.district
        order.city = self.request.user.city
        order.county = self.request.user.county
        order.rural = self.request.user.rural
        order.address = self.request.user.address
        order.postal_code = self.request.user.postal_code

        order.save()

        return order

    def get(self, request, *args, **kwargs):
        cart = Cart.objects.get(user=self.request.user)
        cart_items = CartItem.objects.filter(cart=cart)

        if cart_items.exists():
            order = self.create_order(cart.totalPrice(),cart_items)
            self.request.session['order_id'] = order.id
            return redirect('checkout')
        return redirect('cart-items')



class CheckOutView(LoginRequiredMixin, CustomerRequiredMixin, View):
    template_name = 'order/CheckOut/checkout.html'

    def get(self, request):
        order_id = self.request.session.get('order_id')  # order already created
        if order_id is None:
            return redirect('cart-items')
        order = get_object_or_404(Order, id=order_id)
        provinces = Province.objects.all()
        context = {'order':order,'provinces':provinces}
        return render(request, self.template_name, context)

    def post(self, request):
        order_id = self.request.session.get('order_id')
        if order_id is None:
            return redirect('cart-items')

        order = get_object_or_404(Order, id=order_id)
        form = ExtraOrderInfoForm(request.POST)
        if form.is_valid():
            order.description = form.cleaned_data['description']
            order.save()
            return redirect('zarinpal:send-request')
        context = {'form': form}
        return render(request, self.template_name, context)


class UpdateOrderAddressView(LoginRequiredMixin, CustomerRequiredMixin, View):

    def post(self, request):
        order_id = self.request.session.get('order_id')
        if order_id is None:
            return redirect('cart-items')
        order = get_object_or_404(Order, id=order_id)
        form = OrderAddressForm(request.POST)
        if form.is_valid():
            order.province = form.cleaned_data['province']
            order.county = form.cleaned_data['county']
            order.district = form.cleaned_data['district']
            order.city = form.cleaned_data['city']
            order.rural = form.cleaned_data['rural']
            order.address = form.cleaned_data['address']
            order.postal_code = form.cleaned_data['postal_code']
            order.save()
        return redirect('checkout')





class CancelOrderView(LoginRequiredMixin, CustomerRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        order_id = self.kwargs.get('order_id')
        order = get_object_or_404(Order, id=order_id)
        order.status = 'canceled'
        order.save()
        return redirect('customer-order-history')


class ResumePaymentView(LoginRequiredMixin, CustomerRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        order_id = self.kwargs.get('order_id')
        order = get_object_or_404(Order, id=order_id)
        self.request.session['order_id'] = order.id
        return redirect('checkout')


class PaymentFailedView(LoginRequiredMixin, CustomerRequiredMixin, View):
    template_name = 'order/PaymentFailed/payment-failed.html'

    def get(self, request):
        return render(request, self.template_name)


class PaymentSucceededView(LoginRequiredMixin, CustomerRequiredMixin, View):
    template_name = 'order/PaymentSucceeded/payment-succeeded.html'

    def get(self, request):
        order = Order.objects.get(id=request.session['order_id'])
        print('order in payment succeeded :', order)
        context = {'order': order}


        message = f' {order.user.first_name +" "}عزیز سفارش شما با  موفقیت ثبت شد '
        sms_sender = SmsSender()
        # sms_sender.send_sms(
        #     to=order.user.username,
        #     message=message
        # )
        # request.session['order_id'] = None
        return render(request, self.template_name, context)
