from django import forms
from GOODstime.models import Comment, Favorite, Inquiry, Post, Message, Report, Review
from accounts.models import User

class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ('work_name', 'content', 'tag1', 'tag2', 'tag3', 'give_character', 'want_character', 'price', 'type_transaction', 'type_transfer', 'image1', 'image2', 'image3')

        widgets = {
            'work_name':forms.Textarea(attrs={'cols': '50', 'rows': '1'}),
            'tag1':forms.Textarea(attrs={'cols': '50', 'rows': '1'}),
            'tag2':forms.Textarea(attrs={'cols': '50', 'rows': '1'}),
            'tag3':forms.Textarea(attrs={'cols': '50', 'rows': '1'}),
            'give_character':forms.Textarea(attrs={'cols': '50', 'rows': '1'}),
            'want_character':forms.Textarea(attrs={'cols': '50', 'rows': '1'}),
        }

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

        widgets = {
            'nic_name':forms.Textarea(attrs={'cols': '50', 'rows': '1', 'placeholder': 'サムライ'}),
            'name':forms.Textarea(attrs={'cols': '50', 'rows': '1', 'placeholder': '侍　花子'}),
            'postal_code':forms.Textarea(attrs={'cols': '50', 'rows': '1', 'placeholder': '5555555(ハイフンなし)'}),
            'address':forms.Textarea(attrs={'cols': '50', 'rows': '1', 'placeholder': '東京都千代田区霞が関…'}),
            'phone_number':forms.Textarea(attrs={'cols': '50', 'rows': '1', 'placeholder': '09011112222(ハイフンなし)'}),
            'email':forms.Textarea(attrs={'cols': '50', 'rows': '1', 'placeholder': 'test@example.com'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # formにCSSをあてる
        for field in self.fields.values():
            field.widget.attrs['class'] = 'form-control'

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['content']
        widgets = {
            'content': forms.Textarea(attrs={'rows': 3, 'placeholder': 'コメントを入力してください...'}),
        }
        labels = {
            'content': '',  # ラベルを非表示にする
        }

class MessageForm(forms.ModelForm):
    class Meta:
        model = Message
        fields = ['content']
        widgets = {
            'content': forms.Textarea(attrs={'rows': 1, 'placeholder': '何か入力してください...'}),
        }
        labels = {
            'content': '',  # ラベルを非表示にする
        }

class ReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = ['score', 'comment']
        widgets = {
            'comment': forms.Textarea(attrs={'cols': '100', 'rows': 3, 'placeholder': 'お礼のコメントを書くと喜ばれます'}),
        }
        labels = {
            'comment': '',  # ラベルを非表示にする
            'score': '',  # ラベルを非表示にする
        }
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # formにCSSをあてる
        for field in self.fields.values():
            field.widget.attrs['class'] = 'form-control'

class ReportForm(forms.ModelForm):
    class Meta:
        model = Report
        fields = ['comment']
        widgets = {
            'comment': forms.Textarea(attrs={'cols': '100', 'rows': 3, 'placeholder': '通報内容を記載してください'}),
        }
        labels = {
            'comment': '',  # ラベルを非表示にする
        }

class InquiryForm(forms.ModelForm):
    class Meta:
        model = Inquiry
        fields = ('name', 'email', 'content')

        widgets = {
            'name':forms.Textarea(attrs={'cols': '50', 'rows': '1'}),
            'email':forms.Textarea(attrs={'cols': '50', 'rows': '1'}),
            'content':forms.Textarea(attrs={'cols': '50', 'rows': '7'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # formにCSSをあてる
        for field in self.fields.values():
            field.widget.attrs['class'] = 'form-control'