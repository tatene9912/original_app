from django.urls import path
from . import views

app_name = 'accounts'

urlpatterns = [
    path('accounts/signup/', views.CustomSignupView.as_view(), name='account_signup'),
]
