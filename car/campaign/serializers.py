from campaign.models import Car, Campaign
from rest_framework import serializers


class CarSerializer(serializers.ModelSerializer):
    # entity_instance = EntityInstanceSerializer(many=True)
    class Meta:
        model = Car
        fields = '__all__'
        # fields = ['id','driver_name','phone','bank_name','bank_branch','bank_account']

class ReportSerializer(serializers.ModelSerializer):
    # entity_instance = EntityInstanceSerializer(many=True)
    class Meta:
        model = Car
        fields = ['id']
        # fields = ['id','driver_name','phone','bank_name','bank_branch','bank_account']
