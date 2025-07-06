
from django.urls import path,include
from .views import *

urlpatterns = [
    path('about/', AboutUsView.as_view(), name='about-us'),
    path('privacy-policy/', PrivacyPolicyView.as_view(), name='privacy-policy'),
    path('term-of-use/', TermsOfUseView.as_view(), name='term-of-use'),
    path('faq/', FAQView.as_view(), name='faq'),
    path('contact/', ContactUsView.as_view(), name='contact-us'),
    path('message/', MessagesView.as_view(), name='message-view'),

]