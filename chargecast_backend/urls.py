"""
URL configuration for chargecast_backend project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
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
from django.urls import path

from carbon import views as carbon_views

urlpatterns = [
    path(
        "admin/", admin.site.urls
    ),
    path(
        "api/v1/health/", carbon_views.health, name="health"
    ),
    path(
        "api/v1/carbon/regional/history-7d/",
        carbon_views.regional_history_7d,
        name="carbon-regional-history-7d",
    ),
    path(
        "api/v1/carbon/regional/current-30m/",
        carbon_views.regional_current_30m,
        name="carbon-regional-current-30m",
    ),
    path (
        "api/v1/carbon/regional/forecast-48h/",
        carbon_views.regional_forecast_48h,
        name="carbon-regional-forecast-48h",
    ),
]
