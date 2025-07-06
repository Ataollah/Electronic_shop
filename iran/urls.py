from .views import *
from django.urls import path,include

urlpatterns = [
    path('api/counties/', CountyList.as_view(), name='api-counties'),
    path('api/cities/', CityList.as_view(), name='api-cities'),
    path('api/districts/', DistrictList.as_view(), name='api-districts'),
    path('api/rurals/', RuralList.as_view(), name='api-rurals'),
]