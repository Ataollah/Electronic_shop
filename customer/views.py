# Create your views here.
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import TemplateView,View
from django.shortcuts import render, redirect
from appuser.forms import ProfileForm, ChangePasswordForm
from appuser.mixin import CustomerRequiredMixin
from order.forms import OrderAddressForm
from order.models import Order, OrderPayment
from django.core.paginator import Paginator
from iran.models import Province
from django.utils import timezone
from datetime import timedelta

class DashboardHomeView(LoginRequiredMixin,CustomerRequiredMixin, View):
    template_name = 'customer/Home/home.html'

    def get(self, request):
        return render(request, self.template_name)



class ProfileView(LoginRequiredMixin,CustomerRequiredMixin, View):
    template_name = 'customer/Profile/profile.html'

    def get(self, request, *args, **kwargs):
        user = self.request.user
        initial = {'username': user.username, 'first_name': user.first_name,
                   'last_name': user.last_name,'province': user.province,
                    'city': user.city, 'district': user.district,'email':user.email,
                   'county': user.county, 'rural': user.rural,'profile_picture': user.profile_picture,
                   'address': user.address, 'postal_code': user.postal_code}
        form = ProfileForm(initial=initial)
        provinces = Province.objects.all()
        context = {'form': form,'provinces':provinces}
        return render(request, self.template_name, context)

    def post(self, request):
        user = self.request.user
        provinces = Province.objects.all()
        form = ProfileForm(request.POST,request.FILES, instance=user)
        if form.is_valid():
            form.save()
        else:
            print('profile update form error : ',form.errors)
        context = {'form': form, 'provinces': provinces}
        return render(request, self.template_name, context)

class UpdateUserAddressView(LoginRequiredMixin, CustomerRequiredMixin, View):

    def post(self, request):
        form = OrderAddressForm(request.POST)
        user = request.user
        if form.is_valid():
            user.province = form.cleaned_data['province']
            user.county = form.cleaned_data['county']
            user.district = form.cleaned_data['district']
            user.city = form.cleaned_data['city']
            user.rural = form.cleaned_data['rural']
            user.address = form.cleaned_data['address']
            user.postal_code = form.cleaned_data['postal_code']
            user.save()
        return redirect('customer-profile')


class OrderHistoryView(LoginRequiredMixin,CustomerRequiredMixin, TemplateView):
    template_name = 'customer/OrderHistory/order_history.html'


    def get(self, request, *args, **kwargs):
        user = self.request.user
        orders = Order.objects.filter(user=user).order_by('-created_at')
        paginator = Paginator(orders, 15)  # Show 15 orders per page
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)
        context = {'page_obj': page_obj}
        return render(request, self.template_name, context)

class OrderHistoryByStatusView(LoginRequiredMixin,CustomerRequiredMixin, TemplateView):
    template_name = 'customer/OrderHistory/order_history.html'

    def get(self, request, *args, **kwargs):
        user = self.request.user
        status = kwargs.get('status')  # Assuming 'status' is passed in kwargs
        orders = Order.objects.filter(user=user, status=status).order_by('-created_at')
        paginator = Paginator(orders, 15)  # Show 15 orders per page
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)
        context = {'page_obj': page_obj}
        return render(request, self.template_name, context)


class OrderDetailView(LoginRequiredMixin,CustomerRequiredMixin, View):
    template_name = 'customer/OrderDetails/order_details.html'

    def get(self, request, order_id):
        user = self.request.user
        order = Order.objects.filter(user=user, id=order_id).first()
        payments = OrderPayment.objects.filter(order=order).order_by('-created_at')
        if order is None:
            return redirect('customer-order-history')
        context = {'order': order,'payments': payments}
        return render(request, self.template_name, context)


class ChangePasswordView(LoginRequiredMixin,CustomerRequiredMixin, View):
    template_name = 'customer/ChangePassword/change_password.html'

    def get(self, request):
        form = ChangePasswordForm(request.user)
        context = {'form': form}
        return render(request, self.template_name, context)

    def post(self, request):
        form = ChangePasswordForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            print("Password changed, updating session auth hash")
            update_session_auth_hash(request, user)
            return redirect('customer-dashboard')
        else:
            print("Form errors:", form.errors)
        context = {'form': form}
        return render(request, self.template_name, context)











