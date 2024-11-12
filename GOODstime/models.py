from django.db import models

transaction_CHOICES = [
    (1, '交換'),
    (2, '譲渡'),
]
transfer_CHOICES = [
    (1, '郵送'),
    (2, '手渡し'),
]

class Post(models.Model):
    work_name = models.CharField(max_length=50, verbose_name='作品名')
    content = models.TextField(verbose_name='本文')
    tag1 = models.CharField(max_length=50, verbose_name='タグ1')
    tag2 = models.CharField(max_length=50, verbose_name='タグ2', blank=True)
    tag3 = models.CharField(max_length=50, verbose_name='タグ3', blank=True)
    give_character = models.CharField(max_length=50, verbose_name='譲渡キャラ名')
    want_character = models.CharField(max_length=50, verbose_name='希望キャラ名')
    price = models.IntegerField(verbose_name='価格')
    type_transaction = models.PositiveIntegerField(verbose_name='交換or譲渡',choices=transaction_CHOICES)
    type_transfer = models.PositiveIntegerField(verbose_name='郵送or手渡し',choices=transfer_CHOICES)
    image1 = models.ImageField(verbose_name='画像1')
    image2 = models.ImageField(verbose_name='画像2', blank=True)
    image3 = models.ImageField(verbose_name='画像3', blank=True)
    created_at = models.DateTimeField(verbose_name='作成日時', auto_now_add=True)
    updated_at = models.DateTimeField(verbose_name='更新日時', auto_now=True)

    def __str__(self):
        return self.name