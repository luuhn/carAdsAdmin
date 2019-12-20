from campaign.models import Car, Campaign, CarKpi,Report, ReportImage
from django.contrib.auth.models import User
from rest_framework import serializers


class CamSerializer(serializers.ModelSerializer):
    # entity_instance = EntityInstanceSerializer(many=True)
    class Meta:
        model = Campaign
        fields = '__all__'
class CarDiViceSerializer(serializers.Serializer):
    plate_num = serializers.CharField(max_length=10)
    id  = serializers.CharField(max_length=10)
    campaign_id = serializers.CharField(max_length=10)

class ReportImageSerializer(serializers.Serializer):
    car__driver_name = serializers.CharField(max_length=100)
    car__plate_num = serializers.CharField(max_length=10)
    image_odo = serializers.URLField(max_length=500)
    image_drive = serializers.URLField(max_length=500)
    image_pass = serializers.URLField(max_length=500)
    image_plate = serializers.URLField(max_length=500)

class ReportCamListSerializer(serializers.ModelSerializer):
    # entity_instance = EntityInstanceSerializer(many=True)
    class Meta:
        model = Report
        fields = '__all__'

class CarSerializer(serializers.ModelSerializer):
    # entity_instance = EntityInstanceSerializer(many=True)
    class Meta:
        model = Car
        fields = '__all__'
        # fields = ['id','driver_name','phone','bank_name','bank_branch','bank_account']

class CamSerializer(serializers.ModelSerializer):
    # entity_instance = EntityInstanceSerializer(many=True)
    class Meta:
        model = Campaign
        fields = '__all__'
        # fields = ['id','driver_name','phone','bank_name','bank_branch','bank_account']

class UserSerializer(serializers.ModelSerializer):
    # entity_instance = EntityInstanceSerializer(many=True)
    class Meta:
        model = User
        fields = '__all__'
        # fields = ['id','driver_name','phone','bank_name','bank_branch','bank_account

class ReportSerializer(serializers.ModelSerializer):
    # entity_instance = EntityInstanceSerializer(many=True)
    class Meta:
        model = Car
        fields = ['id']
        # fields = ['id','driver_name','phone','bank_name','bank_branch','bank_account']
class CarKpiSerializer(serializers.ModelSerializer):
    # entity_instance = EntityInstanceSerializer(many=True)
    class Meta:
        model = CarKpi
        fields = '__all__'
