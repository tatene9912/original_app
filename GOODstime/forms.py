from django import forms
from GOODstime.models import Favorite, Post
from accounts.models import User

class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ('work_name', 'content', 'tag1', 'tag2', 'tag3', 'give_character', 'want_character', 'price', 'type_transaction', 'type_transfer', 'image1', 'image2', 'image3')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # formにCSSをあてる
        for field in self.fields.values():
            field.widget.attrs['class'] = 'form-control'

class FavoriteForm(forms.ModelForm):
    class Meta:
        model = Favorite
        fields = [] 

class ProfileForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ('email', 'nic_name', 'image', 'name', 'profile', 'postal_code', 'address', 'phone_number')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # formにCSSをあてる
        for field in self.fields.values():
            field.widget.attrs['class'] = 'form-control'