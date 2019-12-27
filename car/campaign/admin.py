from django.contrib import admin

# Register your models here.

from campaign.models import (Location, Campaign, Car, Report, CampaignCar, ReportImage, UserCampaign)
admin.site.register(Location)
admin.site.register(Campaign)
admin.site.register(Report)
class CampaignCarAdmin(admin.ModelAdmin):
    list_display = ('car', 'campaign')
    search_fields = ['car__plate_num']
    list_filter = ('campaign',)
admin.site.register(CampaignCar, CampaignCarAdmin)
admin.site.register(Car)
class ReportImageAdmin(admin.ModelAdmin):
    search_fields = ['car__plate_num']
    list_display = ('car', 'image_odo_thumbnail','odo_aproved','image_drive_thumbnail','drive_aproved','image_pass_thumbnail','pass_aproved','image_plate_thumbnail','plate_aproved')
    list_editable = ('odo_aproved','drive_aproved','pass_aproved','plate_aproved')
admin.site.register(ReportImage,ReportImageAdmin)
admin.site.register(UserCampaign)
