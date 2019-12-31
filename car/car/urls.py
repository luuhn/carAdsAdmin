"""car URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from rest_framework import routers
from campaign import views

router = routers.DefaultRouter()
router.register(r'cars', views.CarViewSet)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('list/', views.PurchaseList.as_view()),
    path('userlist/', views.UserList.as_view()),
    path('reportlist/', views.ReportCamList.as_view()),
    path('cdivicelist/', views.CarDiviceList.as_view()),
    path('imagelist/', views.ReportImageList.as_view()),
    path('camlist/', views.CamList.as_view()),
    path('carkpi/', views.CarKpiList.as_view()),
    path('camdashboard/', views.CamKpi.as_view()),
    path('districtkpi/', views.CamDistKpi.as_view()),
    path('report/', views.ReportList.as_view()),
    path('report_create/', views.ReportCreate.as_view()),
    path('api_post/', views.api_post, name='vote'),
    path('', include(router.urls)),
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework'))
]
