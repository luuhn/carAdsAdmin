from django.shortcuts import render
from campaign.models import Car, Report, ReportImage,CampaignCar,CarKpi
from campaign.serializers import CarSerializer, ReportSerializer, CarKpiSerializer, UserSerializer
from rest_framework import viewsets, generics
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from django.core import serializers
from django_filters.rest_framework import DjangoFilterBackend
from django.http import JsonResponse
from rest_framework.authentication import SessionAuthentication, BasicAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
# Create your views here.


class UserList(APIView):
    def post(self, request, format=None):
        data =[]
        # car = User.objects.filter(username=request.data["username"])
        user = authenticate(username=request.data["username"], password=request.data["password"])
        if user is not None:
            car = User.objects.filter(username=request.data["username"])
            serializer = UserSerializer(car, many=True)
            data = serializer.data
            print(data)
        return Response(data,status=status.HTTP_200_OK)


class CarViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """

    queryset = Car.objects.all().order_by('plate_num')
    serializer_class = CarSerializer


class PurchaseList(APIView):
    def post(self, request, format=None):
        car = Car.objects.filter(plate_num=request.data["username"])
        serializer = CarSerializer(car, many=True)
        data = serializer.data
        print(data);
        return Response(data[0],status=status.HTTP_200_OK)

class CarKpiList(APIView):
    def post(self, request, format=None):
        car = CarKpi.objects.filter(car__id=request.data["id"])
        serializer = CarKpiSerializer(car, many=True)
        data = serializer.data
        print(data)
        return Response(data[0],status=status.HTTP_200_OK)

class ReportList(APIView):
    def post(self, request, format=None):
        need_report = False
        campaign = CampaignCar.objects.filter(car__id = request.data["id"]).values("campaign")
        if (len(campaign) >0):
            campaign_id = (campaign[0]["campaign"])
            report = Report.objects.filter(campaign__id =campaign_id).order_by('-id')
            if(len(report.values("id"))>0):
                need_report = True
                report_id = report.values("id")[0]["id"]
                image_report = ReportImage.objects.filter(car__id=request.data["id"], report__id=report_id, drive_aproved=True, pass_aproved=True, odo_aproved=True, plate_aproved=True)
                print(image_report.values("id"))
                if(len(image_report.values("id"))>0):
                    need_report = False
        if(need_report):
            serializer = ReportSerializer(report, many=True)
            data = serializer.data
        else:
            data = [{}]
        return Response(data[0],status=status.HTTP_200_OK)

class ReportCreate(APIView):
    def post(self, request, format=None):
        index = int(request.data["index"])
        check_exist = ReportImage.objects.filter(car__id=request.data["id"], report__id= request.data["report_id"])
        if(len(check_exist.values("id")) > 0):
            print(index)
            if (index == 0):
                ReportImage.objects.filter(car__id=request.data["id"], report__id= request.data["report_id"]).update(image_odo=request.data["url"])
            elif (index == 1):
                ReportImage.objects.filter(car__id=request.data["id"], report__id= request.data["report_id"]).update(image_drive=request.data["url"])
            elif (index ==2):
                ReportImage.objects.filter(car__id=request.data["id"], report__id= request.data["report_id"]).update(image_pass=request.data["url"])
            else:
                ReportImage.objects.filter(car__id=request.data["id"], report__id= request.data["report_id"]).update(image_plate=request.data["url"])

        else:
            if (index == 0):
                ReportImage.objects.create(car_id=request.data["id"], report_id= request.data["report_id"],image_odo=request.data["url"])
            elif (index == 1):
                ReportImage.objects.create(car_id=request.data["id"], report_id= request.data["report_id"],image_drive=request.data["url"])
            elif (index == 2):
                ReportImage.objects.create(car_id=request.data["id"], report_id= request.data["report_id"],image_pass=request.data["url"])
            else:
                ReportImage.objects.create(car_id=request.data["id"], report_id= request.data["report_id"],image_plate=request.data["url"])
        return Response({'data':'OK'},status=status.HTTP_200_OK)

@api_view(['POST'])
def api_post(request):
    print (request.data)
    username = request.data['username']
    queryset = Car.objects.filter(plate_num=username)
    serializer = CarSerializer(queryset, many=True)
    if queryset:
        return Response(serializer.data, status=status.HTTP_200_OK)
    else:
        return Response({'error':'Wrong username and password'}, status=status.HTTP_200_OK)
