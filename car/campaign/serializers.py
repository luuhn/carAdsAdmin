from campaign.models import Car, Campaign
from rest_framework import serializers


class CarSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Car
        fields = ['url', 'plate_num', 'password']
