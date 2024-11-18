from django.contrib import admin
from allauth.account import views
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('GOODstime.urls')),
    path("accounts/", include("allauth.urls")),
]
