from django.shortcuts import render
from campaign.models import Car, Report, ReportImage,CampaignCar,CarKpi,UserCampaign,Campaign, CampaignKpi
from campaign.serializers import CarSerializer, ReportSerializer, CarKpiSerializer, UserSerializer, CamSerializer, ReportImageSerializer, ReportCamListSerializer, CarDiViceSerializer
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
from django.db import connection
import json
from django.db.models import Sum
import pandas as pd
import numpy as np
# Create your views here.



class CarDiviceList(APIView):
    def post(self, request, format=None):
        data =[]
        with connection.cursor() as cursor:
             cursor.execute("select c.plate_num,t.id,p.campaign_id from tc_devices t, campaign_car c, campaign_campaigncar p where t.name=p.deviceid and c.id=p.car_id")
             rows = cursor.fetchall()
             result = []
             keys = ('plate_num','deviceId','campaignId',)
             for row in rows:
                 result.append(dict(zip(keys,row)))
                 json_data = json.dumps(result)
        return Response(result,status=status.HTTP_200_OK)


class UserList(APIView):
    def post(self, request, format=None):
        data =[]
        # car = User.objects.filter(username=request.data["username"])
        user = authenticate(username=request.data["username"], password=request.data["password"])
        if user is not None:
            car = User.objects.filter(username=request.data["username"])
            serializer = UserSerializer(car, many=True)
            data = serializer.data
        return Response(data,status=status.HTTP_200_OK)

class CamList(APIView):
    def post(self, request, format=None):
        # car = User.objects.filter(username=request.data["username"])
        cam_id = UserCampaign.objects.filter(user=request.data["username"]).values_list('campaign')
        cam = Campaign.objects.filter(id__in = cam_id)
        serializer = CamSerializer(cam, many=True)
        data = serializer.data
        return Response(data,status=status.HTTP_200_OK)

class ReportCamList(APIView):
    def post(self, request, format=None):
        # car = User.objects.filter(username=request.data["username"])
        report = Report.objects.filter(campaign = request.data["username"])
        serializer = ReportCamListSerializer(report, many=True)
        data = serializer.data
        return Response(data,status=status.HTTP_200_OK)

class ReportImageList(APIView):
    def post(self, request, format=None):
        # car = User.objects.filter(username=request.data["username"])
        report = ReportImage.objects.filter(report = request.data["username"]).values(
        'car__driver_name', 'car__plate_num','image_odo','image_drive','image_pass','image_plate')

        serializer = ReportImageSerializer(report, many=True)
        data = serializer.data
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
        print(data)
        return Response(data[0],status=status.HTTP_200_OK)

class CarKpiList(APIView):
    def post(self, request, format=None):
        # car = CarKpi.objects.filter(campaign_id=request.data["camid"]).values('car','totalDistance','impression','province')

        # df=pd.DataFrame(car)
        # # print(df['province'])
        # if 'Ho' in str(df['province']):
        # # if df['province'].str.contains("Ho"):
        #     df['inside']=0
        # else:
        #     df['inside']=df['totalDistance']
        # d=df.groupby(['car'])['totalDistance','inside','impression'].sum()
        #tmp run
        cam= Campaign.objects.get(pk=request.data["camid"])
        cityname= cam.location.name
        cursor = connection.cursor()
        cursor.execute("select car_id,sum(totalDistance),sum(impression) from campaign_carkpi where campaign_id=%s group by car_id",[request.data["camid"]])
        rows = cursor.fetchall()
        result = []
        keys = ('plate','totalDistance','impression','inside',)
        for row in rows:
            #get inside
            data=[]
            kq=CarKpi.objects.filter(car_id=row[0],province__icontains=cityname).values('car__plate_num').annotate(score =Sum('totalDistance'))
            # print(kq[0])
            if kq:
                data.append(kq[0]['car__plate_num'])
                data.append(row[1])
                data.append(row[2])
                data.append(kq[0]['score'])
                result.append(dict(zip(keys,data)))
        return Response(result,status=status.HTTP_200_OK)

class CamDistKpi(APIView):
    def post(self, request, format=None):
        cam= Campaign.objects.get(pk=request.data["camid"])
        cityname= cam.location.name
        result = []
        listkpi=CampaignKpi.objects.filter(campaign_id=request.data["camid"],province__icontains=cityname).values('district').annotate(score =Sum('totalDistance'))[:15]
        keys = ('name','value',)
        for lk in listkpi:
            data=[]
            data.append(lk['district'])
            data.append(lk['score'])
            result.append(dict(zip(keys,data)))
        return Response(result,status=status.HTTP_200_OK)

class CamKpi(APIView):
    def post(self, request, format=None):
        cam= Campaign.objects.get(pk=request.data["camid"])
        cityname= cam.location.name
        result = []
        camkpi=CarKpi.objects.filter(campaign_id=request.data["camid"]).values()
        df=pd.DataFrame(camkpi)
        # print(df)
        total = df['totalDistance'].sum()
        impress=df['impression'].sum()
        
        maxcar=df.groupby(['car_id'])['totalDistance'].sum().max()
        avgcar=df.groupby(['car_id'])['totalDistance'].sum().mean()
        countcar=df.groupby(['car_id'])['totalDistance'].sum().count()
        cammaxkm= cam.maxkm*countcar
        cammaximpress=cam.maxkm*80*countcar
        percentkm=int((total/cammaxkm)*100)
        percentimpress=int((impress/cammaximpress)*100)
        if percentkm>100:
            percentkm=100
        if percentimpress>100:
            percentimpress=100
        print(percentimpress)
        # print(avgcar)
        #top car kpi
        keys = ('id','plate','km','impression','city',)
        kq=CarKpi.objects.filter(campaign_id=request.data["camid"]).values('car__plate_num').annotate(score =Sum('totalDistance')).annotate(score1 =Sum('impression')).order_by('-score')[:5]
        for k in kq:
            # print(k)
            data=[]
            data.append(k['car__plate_num'])
            data.append(str(k['car__plate_num']))
            data.append(str(k['score']))
            data.append(str(k['score1']))
            data.append(str(cityname))
            result.append(dict(zip(keys,data)))
        # for kpi in camkpi:
        # print(result)
        return Response({'total':int(total),'impress':int(impress),'maxcar':int(maxcar),'avgcar':int(avgcar),'countcar':countcar,'topkpi':result,'camname':cam.name,'percentkm':percentkm,'percentimpress':percentimpress},status=status.HTTP_200_OK)



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
