from allauth.account.forms import SignupForm
from django import forms

class CustomSignupForm(SignupForm):
    name = forms.CharField(
        label="氏名",
        max_length=50,
        widget=forms.TextInput(attrs={'placeholder': '侍 花子'})
    )
    nic_name = forms.CharField(
        label="ニックネーム",
        max_length=50,
        widget=forms.TextInput(attrs={'placeholder': 'サムライ'})
    )
    postal_code = forms.CharField(
        label="郵便番号",
        max_length=7,
        widget=forms.TextInput(attrs={'placeholder': '5555555(ハイフンなし)'})
    )
    address = forms.CharField(
        label="住所",
        max_length=100,
        widget=forms.TextInput(attrs={'placeholder': '東京都千代田区霞が関…'})
    )
    phone_number = forms.CharField(
        label="電話番号",
        max_length=15,
        widget=forms.TextInput(attrs={'placeholder': '09011112222(ハイフンなし)'})
    )

    def signup(self, request, user):
        """新規登録時に追加データを保存"""
        user.name = self.cleaned_data['name']
        user.nic_name = self.cleaned_data['nic_name']
        user.postal_code = self.cleaned_data['postal_code']
        user.address = self.cleaned_data['address']
        user.phone_number = self.cleaned_data['phone_number']
        user.save()
        return user
