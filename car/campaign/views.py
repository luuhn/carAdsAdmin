from django.shortcuts import render
from campaign.models import Car
from campaign.serializers import CarSerializer
from rest_framework import viewsets
# Create your views here.

class CarViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    queryset = Car.objects.all().order_by('plate_num')
    serializer_class = CarSerializer
