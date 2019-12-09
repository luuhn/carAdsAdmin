from django.contrib import admin

# Register your models here.

from campaign.models import (Location, Campaign, Car, Report, CampaignCar, ReportImage)
admin.site.register(Location)
admin.site.register(Campaign)
admin.site.register(Report)
admin.site.register(CampaignCar)
admin.site.register(Car)
admin.site.register(ReportImage)
