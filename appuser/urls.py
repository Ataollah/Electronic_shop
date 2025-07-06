from django.urls import path,include
from appuser.views.views import *
from appuser.views.api_views import *

urlpatterns = [
    path('login/',LoginView.as_view(),name='login-view'),
    path('logout', LogoutView.as_view(), name='logout-view'),
    path("candid-phone-verification/", CandidPhoneVerificationView.as_view(), name="candid-phone-verification-view"),

    path('verify-candid-code/',VerifyCandidCodeView.as_view(),name='verify-candid-code-view'),
    path('create-user/', CreateUserView.as_view(), name='create-user-view'),
    path('create-user-succeeded/', CreatedUserSucceededView.as_view(), name='create-user-succeeded-view'),
    path('user-phone-verification/',UserPhoneVerificationView.as_view(),name='user-phone-verification-view'),
    # path('candid-send-code', SendCodeToCandidUserView.as_view(), name='send-code-candid-user-view'),
    path('verify-user-code/', VerifyUserCodeView.as_view(), name='verify-user-code-view'),

    path('reset-password/',ResetPasswordView.as_view(),name='reset-password-view'),

    path('reset-pass-done/',ResetPasswordDoneView.as_view(),name='reset-password-done-view'),

    path('sendcode_api/', SendCode.as_view(), name='send-code-api'),
    path('sendcode_candiduser/', SendCodeToCandidUser.as_view(), name='send-code-to-candid-api'),
    path('sendcode_user/', SendCodeToUser.as_view(), name='send-code-to-user-api'),

]