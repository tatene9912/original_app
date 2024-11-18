from allauth.account.forms import SignupForm
from django import forms
from .models import User
from allauth.account.adapter import DefaultAccountAdapter

class CustomSignupForm(SignupForm):
    name = forms.CharField()
    nic_name = forms.CharField()
    postal_code = forms.CharField()
    address = forms.CharField()
    phone_number = forms.CharField()
    
    class Meta:
        model = User

    def signup(self, request,user):
        user.name = self.cleaned_data['name']
        user.nic_name = self.cleaned_data['nic_name']
        user.postal_code = self.cleaned_data['postal_code']
        user.address = self.cleaned_data['address']
        user.phone_number = self.cleaned_data['phone_number']
        user.save()
        return user