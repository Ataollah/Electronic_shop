import datetime
import pytest
from django.core.files.uploadedfile import SimpleUploadedFile
from product.models import *


def create_product_image():
    return SimpleUploadedFile(
        name="test_image.jpg",
        content=b"file_content",
        content_type="image/jpeg"
    )

@pytest.fixture
def category(db):
    return Category.objects.create(
        title="Test Category",
        slug="test-category",
        image=create_product_image(),
        order=1
    )

@pytest.fixture
def product(db, category):
    image_file = SimpleUploadedFile(
        name="test_image.jpg",
        content=b"file_content",
        content_type="image/jpeg"
    )
    return Product.objects.create(
        category=category,
        show_on_homepage=True,
        order=1,
        title="Test Product",
        slug="test-product",
        current_price=100000,
        discount=10,
        old_price=120000,
        inventory=50,
        short_description="Short description",
        description="Full description",
        primary_image=image_file,
        secondary_image=image_file,
        image_tag="tag1,tag2",
        offer_start_date=datetime.date.today(),
        offer_end_date=datetime.datetime.now() + datetime.timedelta(days=10)
    )


@pytest.fixture
def gallery(db, product):
    image_file = SimpleUploadedFile(
        name="gallery_image.jpg",
        content=b"image_content",
        content_type="image/jpeg"
    )
    thumbnail_file = SimpleUploadedFile(
        name="gallery_thumb.jpg",
        content=b"thumb_content",
        content_type="image/jpeg"
    )
    return Gallery.objects.create(
        product=product,
        image=image_file,
        thumbnail=thumbnail_file,
        order=1
    )

@pytest.fixture
def question(db, product):
    return Questions.objects.create(
        product=product,
        question="What is the warranty period?",
        answer="The warranty period is 2 years.",
        order=1
    )

@pytest.fixture
def banner(db, product):
    image_file = SimpleUploadedFile(
        name="banner_image.jpg",
        content=b"banner_image_content",
        content_type="image/jpeg"
    )
    return Banner.objects.create(
        product=product,
        small_title="Small Banner Title",
        big_title="Big Banner Title",
        image=image_file,
        description="Banner description",
        order=1
    )


@pytest.fixture
def about_product(db, product):
    image_file = SimpleUploadedFile(
        name="about_product_image.jpg",
        content=b"about_image_content",
        content_type="image/jpeg"
    )
    return AboutProduct.objects.create(
        product=product,
        title="About Product Title test",
        description="About product description",
        image=image_file,
        direction="RTL",
        order=1
    )

@pytest.fixture
def countdown_banner(db, product):
    image_left = SimpleUploadedFile(
        name="left_image.jpg",
        content=b"left_image_content",
        content_type="image/jpeg"
    )
    image_right = SimpleUploadedFile(
        name="right_image.jpg",
        content=b"right_image_content",
        content_type="image/jpeg"
    )
    return CountDownBanner.objects.create(
        product=product,
        title="Countdown Banner Title",
        image_left=image_left,
        image_right=image_right,
        description="Countdown banner description",
        start_date=datetime.date.today(),
        end_date=datetime.datetime.now() + datetime.timedelta(days=10)
    )


@pytest.fixture
def brand(db):
    image_file = SimpleUploadedFile(
        name="brand_image.jpg",
        content=b"brand_image_content",
        content_type="image/jpeg"
    )
    return Brands.objects.create(
        title="Test Brand",
        image=image_file,
        order=1
    )


@pytest.fixture
def about_after_before_product(product):
    image_before = SimpleUploadedFile(
        name="before_image.jpg",
        content=b"before_image_content",
        content_type="image/jpeg"
    )
    image_after = SimpleUploadedFile(
        name="after_image.jpg",
        content=b"after_image_content",
        content_type="image/jpeg"
    )
    return AboutAfterBeforeProduct.objects.create(
        product=product,
        title="Before and After Title",
        description="Description for before and after product",
        image_before=image_before,
        image_after=image_after
    )