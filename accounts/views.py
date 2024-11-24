from allauth.account.views import SignupView
from django.urls import reverse_lazy
from .forms import CustomSignupForm

class CustomSignupView(SignupView):
    form_class = CustomSignupForm
    template_name = 'accounts/signup.html'  # 使用するテンプレートを指定
    success_url = reverse_lazy('account_login')  # 登録後のリダイレクト先を指定

    def form_valid(self, form):
        response = super().form_valid(form)
        return response
