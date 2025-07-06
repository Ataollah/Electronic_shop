import pytest
from django.core.files.uploadedfile import SimpleUploadedFile

from siteInfo.models import *

@pytest.fixture
def menu(db):
    return Menu.objects.create(
        name='Test Menu',
        url='/test-url/',
        order=1
    )

@pytest.fixture
def submenu(db, menu):
    return SubMenu.objects.create(
        menu=menu,
        name='Test SubMenu',
        url='/test-submenu/',
        order=1
    )

@pytest.fixture
def site_info(db):
    return SiteInfo.objects.create(
        name='Test Website',
        slogan='Test Slogan',
        logo_header=SimpleUploadedFile('logo_header.png', b'file_content', content_type='image/png'),
        logo_footer=SimpleUploadedFile('logo_footer.png', b'file_content', content_type='image/png'),
        email1='test1@example.com',
        email2='test2@example.com',
        address='Test Address',
        telephone1='02112345678',
        telephone2='02187654321',
        copyright='Test Copyright',
        copyright_link='https://wedosoft.ir',
        map_url='https://maps.google.com/?q=tehran',
        enamad_id='123456',
        enamad_tag='<tag>نماد</tag>',
        working_hours='9-18',
        instagram_id='test_instagram',
        is_selling=True
    )

@pytest.fixture
def sms_provider(db):
    return SMSProvider.objects.create(
        name='Test SMS Provider',
        api_url='https://api.smsprovider.com/send',
        username='testuser',
        password='testpass',
        phone_number='09120000000'
    )

@pytest.fixture
def mail_provider(db):
    return MailProvider.objects.create(
        name='Test Mail Provider',
        smtp_sender_email='test@mail.com',
        smtp_sender_password='testpassword',
        smtp_server='smtp.mail.com',
        smtp_port=587
    )

@pytest.fixture
def social_media(db):
    return SocialMedia.objects.create(
        url='https://t.me/testuser',
        type='telegram'
    )

@pytest.fixture
def link(db):
    return Links.objects.create(
        title='Test Link',
        url='https://example.com',
        type='internal'
    )

@pytest.fixture
def contact_us(db):
    return ContactUS.objects.create(
        name='Test User',
        email='testuser@example.com',
        phone='09120000000',
        subject='Test Subject',
        message='This is a test message.'
    )

@pytest.fixture
def faq(db):
    return FAQ.objects.create(
        question='What is your return policy?',
        answer='<p>You can return any item within 30 days.</p>',
        order=1
    )

@pytest.fixture
def gallery(db):
    image_file = SimpleUploadedFile(
        name='gallery_image.jpg',
        content=b'file_content',
        content_type='image/jpeg'
    )
    return Gallery.objects.create(
        title='Sample Gallery',
        image=image_file,
    )

@pytest.fixture
def testimonial(db):
    return Testimonial.objects.create(
        name='Sample User',
        message='<p>This is a testimonial message.</p>',
        order=1
    )

