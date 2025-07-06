from django.shortcuts import render
from iran.models import Province, County, City, District, Rural
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
# Create your views here.



class CountyList(APIView):
    def get(self, request):
        province_id = request.GET.get('province_id')
        counties = County.objects.filter(province_id=province_id).values('id', 'name')
        return Response(list(counties))

class CityList(APIView):
    def get(self, request):
        county_id = request.GET.get('county_id')
        cities = City.objects.filter(county_id=county_id).values('id', 'name')
        return Response(list(cities))

class DistrictList(APIView):
    def get(self, request):
        county_id = request.GET.get('county_id')
        districts = District.objects.filter(county_id=county_id).values('id', 'name')
        return Response(list(districts))

class RuralList(APIView):
    def get(self, request):
        county_id = request.GET.get('county_id')
        rurals = Rural.objects.filter(county_id=county_id).values('id', 'name')
        return Response(list(rurals))
