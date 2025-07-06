import pytest
from zarinpal.models import ZarinPal

@pytest.fixture
def zarinpal(db):
    return ZarinPal.objects.create(
        merchant_id='test-merchant-id',
        request_url='https://api.zarinpal.com/request',
        verify_url='https://api.zarinpal.com/verify',
        start_pay_url='https://www.zarinpal.com/startpay',
        callback_url='https://example.com/callback',
        sandbox=True,
        min_amount=100000
    )