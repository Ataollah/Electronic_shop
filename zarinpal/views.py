from django.conf import settings
from django.shortcuts import redirect
from django.urls import reverse
from django.views.generic import TemplateView
import requests
import json
from order.models import Order, OrderPayment
from django.views import View

# Zarinpal API URLs
sandbox = 'sandbox' if settings.SANDBOX else 'www'
ZP_API_REQUEST = f"https://{sandbox}.zarinpal.com/pg/v4/payment/request.json"
ZP_API_VERIFY = f"https://{sandbox}.zarinpal.com/pg/v4/payment/verify.json"
ZP_API_STARTPAY = f"https://{sandbox}.zarinpal.com/pg/StartPay/"

# ZP_API_REQUEST = f"https://payment.zarinpal.com/pg/v4/payment/request.json"
# ZP_API_VERIFY = f"https://payment.zarinpal.com/pg/v4/payment/verify.json"
# ZP_API_STARTPAY = f"https://payment.zarinpal.com/pg/StartPay/"


CallbackURL = 'http://127.0.0.1:8000/zarinpal/verify/'


# CallbackURL = 'https://shoopeh.ir/zarinpal/verify/'

def save_request_to_zarinpal(order_id, authority):
    order = Order.objects.get(id=order_id)
    OrderPayment.objects.create(order=order, amount=order.total_amount, authority=authority).save()


def save_zarin_payment_result(authority, result_data):
    payment = OrderPayment.objects.get(authority=authority)
    payment.transaction_id = result_data['transaction_id']
    payment.status = result_data['payment_status']
    payment.save()
    payment.order.status = result_data['order_status']
    payment.order.save()
    return payment.order.id


def prepare_request_data(order_id):
    order = Order.objects.get(id=order_id)
    return json.dumps({
        "merchant_id": settings.MERCHANT,
        "amount": order.total_amount,  # Test amount
        "description": f"{order_id} - {order.user.username}",
        "callback_url": CallbackURL,
        "order_id": str(order_id),
        "metadata": {"mobile": order.user.username, "email": order.user.email}
    }), {'content-type': 'application/json'}




class SendRequestView(View):
    def get(self, request, *args, **kwargs):
        order_id = request.session.get('order_id')
        data, headers = prepare_request_data(order_id)
        try:
            response = requests.post(ZP_API_REQUEST, data=data, headers=headers, timeout=10).json()
            if response['data']['code'] == 100:
                save_request_to_zarinpal(order_id, response['data']['authority'])
                return redirect(ZP_API_STARTPAY + response['data']['authority'])
        except Exception:
            pass
        return redirect(reverse('zarinpal:server-error-view'))


class ServerErrorView(TemplateView):
    template_name = 'zarinpal/ServerError/server_error.html'


def prepare_verify_data(authority):
    amount = OrderPayment.objects.get(authority=authority).amount
    return json.dumps({
        "merchant_id": settings.MERCHANT,
        "amount": amount,  # Test amount
        "authority": authority
    }), {'content-type': 'application/json'}


class VerifyRequestView(View):

    def get(self, request, *args, **kwargs):
        authority, status = request.GET.get('Authority'), request.GET.get('Status')
        if status == 'OK':
            data, headers = prepare_verify_data(authority)
            response = requests.post(ZP_API_VERIFY, data=data, headers=headers)
            if response.status_code == 200:
                response_data = response.json()
                result_data = {
                    'transaction_id': response_data['data']['ref_id'],
                    'order_status': 'paid',
                    'payment_status': 'paid'
                }
                if response_data['data']['code'] in [100, 101]:
                    order_id = save_zarin_payment_result(authority, result_data)
                    request.session['order_id'] = order_id
                    return redirect('payment-succeeded-view')

            if response['data']['code'] in [100, 101]:
                order_id = save_zarin_payment_result(authority, {
                    'transaction_id': response['data']['ref_id'],
                    'order_status': 'paid',
                    'payment_status': 'paid'
                })
                request.session['order_id'] = order_id
                return redirect('payment-succeeded-view')
        order_id = save_zarin_payment_result(authority, {
            'transaction_id': '111111',
            'order_status': 'unpaid',
            'payment_status': 'failed'
        })
        request.session['order_id'] = order_id
        return redirect('payment-failed-view')


