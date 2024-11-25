from django.db import models
from accounts.models import User
from django.conf import settings
from django.urls import reverse

transaction_CHOICES = [
    (1, '交換'),
    (2, '譲渡'),
]
transfer_CHOICES = [
    (1, '郵送'),
    (2, '手渡し'),
]
STATUS_CHOICES = [
    ('unmatched', '取引未成立'),
    ('matched', '取引成立'),
    ('completed', '取引完了'),
]

class Post(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE, verbose_name='投稿者名',related_name='posts',null=True)
    work_name = models.CharField(max_length=100, verbose_name='タイトル')
    content = models.TextField(verbose_name='本文')
    tag1 = models.CharField(max_length=50, verbose_name='タグ1')
    tag2 = models.CharField(max_length=50, verbose_name='タグ2', blank=True)
    tag3 = models.CharField(max_length=50, verbose_name='タグ3', blank=True)
    give_character = models.CharField(max_length=50, verbose_name='譲渡キャラ名', blank=True)
    want_character = models.CharField(max_length=50, verbose_name='希望キャラ名', blank=True)
    price = models.IntegerField(verbose_name='価格')
    type_transaction = models.PositiveIntegerField(verbose_name='交換or譲渡',choices=transaction_CHOICES)
    type_transfer = models.PositiveIntegerField(verbose_name='郵送or手渡し',choices=transfer_CHOICES)
    match_user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='マッチングユーザー', related_name='match_posts',null=True, blank=True)
    status = models.CharField(verbose_name='ステータス', max_length=20, choices=STATUS_CHOICES, default='unmatched', blank=True, null=True)
    image1 = models.ImageField(verbose_name='画像1')
    image2 = models.ImageField(verbose_name='画像2', blank=True)
    image3 = models.ImageField(verbose_name='画像3', blank=True)
    created_at = models.DateTimeField(verbose_name='作成日時', auto_now_add=True)
    updated_at = models.DateTimeField(verbose_name='更新日時', auto_now=True)

    def __str__(self):
        return self.work_name

class Comment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='会員名', null=True)
    post = models.ForeignKey(Post, on_delete=models.CASCADE, verbose_name='投稿名', null=True, related_name='comments')
    content = models.TextField(verbose_name='本文')
    created_at = models.DateTimeField(verbose_name='作成日時', auto_now_add=True)

    def __str__(self):
        return f"{self.user.nic_name} at {self.post.user.nic_name}"
    
class Message(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='会員名', null=True)
    post = models.ForeignKey(Post, on_delete=models.CASCADE, verbose_name='投稿名', null=True, related_name='messages')
    content = models.TextField(verbose_name='本文')
    created_at = models.DateTimeField(verbose_name='作成日時', auto_now_add=True)

    def __str__(self):
        return f"{self.user.nic_name} at {self.post.user.nic_name}"
    
review_CHOICES = [
    (1, '良かった'),
    (2, '悪かった'),
]

class Review(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='会員名', null=True, related_name='reviews')
    post = models.ForeignKey(Post, on_delete=models.CASCADE, verbose_name='投稿名', null=True, blank=True)
    target_user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='対象会員名', null=True, related_name='target_reviews')
    score = models.PositiveIntegerField(verbose_name='評価',choices=review_CHOICES)
    comment = models.TextField(verbose_name='コメント',blank=True)
    created_at = models.DateTimeField(verbose_name='作成日時', auto_now_add=True)

    def __str__(self):
        return f"{self.user.nic_name}"
    
class Favorite(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='会員名', null=True)
    post = models.ForeignKey(Post, on_delete=models.CASCADE, verbose_name='投稿名', null=True)
    created_at = models.DateTimeField(verbose_name='作成日時', auto_now_add=True)
    updated_at = models.DateTimeField(verbose_name='更新日時', auto_now=True)

    def __str__(self):
        return f"{self.user.nic_name}"
    
class Report(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='会員名', null=True)
    post = models.ForeignKey(Post, on_delete=models.CASCADE, verbose_name='投稿名', null=True)
    comment = models.TextField(verbose_name='内容',blank=True)
    delete_flg = models.BooleanField(verbose_name='削除フラグ', default=False)
    created_at = models.DateTimeField(verbose_name='作成日時', auto_now_add=True)
    updated_at = models.DateTimeField(verbose_name='更新日時', auto_now=True)

    def __str__(self):
        return f"{self.user.nic_name} at {self.post.user.nic_name}"
    
class Block(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='会員名', null=True, related_name='reports')
    target_user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='対象会員名', null=True, related_name='target_reports')
    created_at = models.DateTimeField(verbose_name='作成日時', auto_now_add=True)
    updated_at = models.DateTimeField(verbose_name='更新日時', auto_now=True)

    def __str__(self):
        return f"{self.user.nic_name}"
    
class Stripe_Customer(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='stripe_customer', verbose_name='会員名')
    stripeCustomerId = models.CharField(max_length=255, verbose_name='カスタマーID')
    stripeSubscriptionId = models.CharField(max_length=255, null=True, blank=True, verbose_name='サブスクリプションID')
    stripePaymentMethodId = models.CharField(max_length=255, null=True, blank=True, verbose_name='支払い方法') 
    created_at = models.DateTimeField(verbose_name='作成日時', auto_now_add=True)
    updated_at = models.DateTimeField(verbose_name='更新日時', auto_now=True)

    def __str__(self):
        return f"Stripe Customer for {self.user.email}"
    
class Admin_user(models.Model):
    name = models.CharField(max_length=50, verbose_name='氏名')
    password = models.CharField(max_length=50, verbose_name='パスワード')
    email = models.EmailField(verbose_name='メールアドレス')
    created_date = models.DateTimeField(verbose_name='作成日時', auto_now_add=True, null=True)
    updated_date = models.DateTimeField(verbose_name='更新日時', auto_now=True, null=True)

    def __str__(self):
        return self.name