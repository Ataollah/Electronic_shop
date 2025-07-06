import io

import pytest
from PIL import Image
from django.contrib.auth.models import Group
from django.core.files.uploadedfile import SimpleUploadedFile
from django.utils import timezone
from appuser.models import VerificationUser
from appuser.models import *

@pytest.fixture
def verification_user(db):
    return VerificationUser.objects.create(
        username="09123456789",
        verification_code="123456",
        valid_until=timezone.now() + timezone.timedelta(hours=1)
    )

@pytest.fixture
def app_user(db):
    image_file = SimpleUploadedFile("test_profile.jpg", b"image")
    return AppUser.objects.create_user(
        profile_picture = image_file,
        username="09111111111",
        password="testpass",
        first_name="Test First name",
        last_name="Test Last name",
        province="تهران",
        county="تهران",
        district="مرکزی",
        city="تهران",
        rural="",
        address="Test address",
        postal_code="1234567890"
    )

@pytest.fixture
def customer_user(db, app_user):
    group =Group.objects.create(name="Customer")
    app_user.groups.add(group)
    return app_user

@pytest.fixture
def cashier_user(db, app_user):
    group = Group.objects.create(name="Cashier")
    app_user.groups.add(group)
    return app_user

@pytest.fixture
def manager_user(db, app_user):
    group = Group.objects.create(name="Manager")
    app_user.groups.add(group)
    return app_user


def get_test_image(filename='test.jpg', size=(10, 10), color='red'):
    image_io = io.BytesIO()
    image = Image.new('RGB', size, color=color)
    image.save(image_io, format='JPEG')
    image_io.seek(0)
    return SimpleUploadedFile(
        name=filename,
        content=image_io.read(),
        content_type='image/jpeg'
    )

