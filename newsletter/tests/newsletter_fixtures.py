import pytest
from newsletter.models import *

@pytest.fixture
def subscriber(db):
    return Subscriber.objects.create(
        email='subscriber@example.com'
    )

@pytest.fixture
def newsletter(db):
    return Newsletter.objects.create(
        subject='Sample Newsletter',
        body='<p>This is the body of the newsletter.</p>',
        send_at=timezone.now()
    )