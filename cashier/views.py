from django.core.paginator import Paginator
from django.shortcuts import render, redirect
from appuser.forms import ChangePasswordForm
from appuser.mixin import CashierRequiredMixin
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import TemplateView, View
from django.urls import reverse
from order.models import Order, OrderPayment
from siteInfo.models import SiteInfo
from Utility.VerificationMessageSender import VerificationMessageSender


# Create your views here.


class DashboardHomeView(LoginRequiredMixin, CashierRequiredMixin, View):
    template_name = 'cashier/Home/home.html'

    def get(self, request):
        pending_orders_count = Order.objects.filter( status='pending').count()
        paid_orders_count = Order.objects.filter( status='paid').count()
        unpaid_orders_count = Order.objects.filter( status='unpaid').count()
        context = {
            'pending_orders_count': pending_orders_count,
            'paid_orders_count': paid_orders_count,
            'unpaid_orders_count': unpaid_orders_count,
        }

        return render(request, self.template_name, context)


def getPersianOrderStatus(status):
    order_dict = dict(Order.ORDER_STATUS)
    status = order_dict.get(status)
    if status:
        return status
    return ''



class OrdersByStatusView(LoginRequiredMixin, CashierRequiredMixin, TemplateView):
    template_name = 'cashier/OrderHistory/order_history.html'

    def get(self, request, *args, **kwargs):
        status = kwargs.get('status')  # Assuming 'status' is passed in kwargs
        if status == 'all':
            orders = Order.objects.all().order_by('-created_at')
        else:
            orders = Order.objects.filter(status=status).order_by('-created_at')
        paginator = Paginator(orders, 15)  # Show 15 orders per page
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)
        context = {'page_obj': page_obj, 'persian_status': getPersianOrderStatus(status)}
        return render(request, self.template_name, context)


class OrderDetailView(LoginRequiredMixin, CashierRequiredMixin, View):
    template_name = 'cashier/OrderDetails/order_details.html'

    def get(self, request, order_id):
        order = Order.objects.filter(id=order_id).first()
        payments = OrderPayment.objects.filter(order=order).order_by('-created_at')
        if order is None:
            return redirect('cashier:dashboard')
        context = {'order': order, 'payments': payments}
        return render(request, self.template_name, context)


class ChangeOrderStatusView(LoginRequiredMixin, CashierRequiredMixin, View):
    template_name = 'cashier/Order/Detail/order_details.html'

    def post(self, request, order_id):
        order = Order.objects.filter(id=order_id).first()
        if order is None:
            return redirect('cashier:dashboard')
        status = request.POST.get('status')
        if status:
            order.status = status
            order.save()

        sender = VerificationMessageSender(order.user.username)
        message = f'مشتری گرامی وضعیت سفارش شماره {order.id} به {order.get_persian_status()} تغییر یافت '
        #sender.send_sms(message)

        # send message to user
        # Redirect to the order detail page or any other page
        return redirect(f'{reverse("cashier:dashboard")}?status={status}')


class ChangePasswordView(LoginRequiredMixin, CashierRequiredMixin, View):
    template_name = 'cashier/ChangePassword/change_password.html'

    def get(self, request):
        form = ChangePasswordForm(request.user)
        context = {'form': form}
        return render(request, self.template_name, context)

    def post(self, request):
        form = ChangePasswordForm(request.user, request.POST)
        if form.is_valid():
            form.save()
            return redirect('cashier:dashboard')
        context = {'form': form}
        return render(request, self.template_name, context)


class ToggleSellingView(LoginRequiredMixin, CashierRequiredMixin, View):
    template_name = 'cashier/ToggleSelling/toggle_selling.html'

    def get(self, request):
        site_info = SiteInfo.objects.all().first()
        is_selling = site_info.is_selling
        context = {'is_selling': is_selling}
        return render(request, self.template_name, context)

    def post(self, request):
        site_info = SiteInfo.objects.all().first()
        site_info.is_selling = not site_info.is_selling
        site_info.save()
        context = {'is_selling': site_info.is_selling}
        return render(request, self.template_name, context)

