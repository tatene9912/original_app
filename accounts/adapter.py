from allauth.account.adapter import DefaultAccountAdapter


class CustomAccountAdapter(DefaultAccountAdapter):

    def is_open_for_signup(self, request):
        # サインアップを許可するかどうかを制御
        return True

    def save_user(self, request, user, form, commit=True):
        # ユーザー情報の保存方法をカスタマイズ
        user = super().save_user(request, user, form, commit=False)
        user.name = form.cleaned_data.get("name")
        user.nic_name = form.cleaned_data.get("nic_name")
        user.postal_code = form.cleaned_data.get("postal_code")
        user.address = form.cleaned_data.get("address")
        user.phone_number = form.cleaned_data.get("phone_number")
        if commit:
            user.save()
        return user

    def confirm_email(self, request, email_address):
        # メール確認プロセスのカスタマイズ
        email_address.verified = True
        email_address.save()
