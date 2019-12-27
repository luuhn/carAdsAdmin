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
admin.site.register(ReportImage)
admin.site.register(UserCampaign)
