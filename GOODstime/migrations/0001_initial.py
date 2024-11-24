# Generated by Django 5.1.3 on 2024-11-18 10:46

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Admin_user',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50, verbose_name='氏名')),
                ('password', models.CharField(max_length=50, verbose_name='パスワード')),
                ('email', models.EmailField(max_length=254, verbose_name='メールアドレス')),
                ('created_date', models.DateTimeField(auto_now_add=True, null=True, verbose_name='作成日時')),
                ('updated_date', models.DateTimeField(auto_now=True, null=True, verbose_name='更新日時')),
            ],
        ),
        migrations.CreateModel(
            name='Block',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='作成日時')),
                ('updated_at', models.DateTimeField(auto_now=True, verbose_name='更新日時')),
                ('target_user', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='target_reports', to=settings.AUTH_USER_MODEL, verbose_name='対象会員名')),
                ('user', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='reports', to=settings.AUTH_USER_MODEL, verbose_name='会員名')),
            ],
        ),
        migrations.CreateModel(
            name='Post',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('work_name', models.CharField(max_length=50, verbose_name='作品名')),
                ('content', models.TextField(verbose_name='本文')),
                ('tag1', models.CharField(max_length=50, verbose_name='タグ1')),
                ('tag2', models.CharField(blank=True, max_length=50, verbose_name='タグ2')),
                ('tag3', models.CharField(blank=True, max_length=50, verbose_name='タグ3')),
                ('give_character', models.CharField(blank=True, max_length=50, verbose_name='譲渡キャラ名')),
                ('want_character', models.CharField(blank=True, max_length=50, verbose_name='希望キャラ名')),
                ('price', models.IntegerField(verbose_name='価格')),
                ('type_transaction', models.PositiveIntegerField(choices=[(1, '交換'), (2, '譲渡')], verbose_name='交換or譲渡')),
                ('type_transfer', models.PositiveIntegerField(choices=[(1, '郵送'), (2, '手渡し')], verbose_name='郵送or手渡し')),
                ('image1', models.ImageField(upload_to='', verbose_name='画像1')),
                ('image2', models.ImageField(blank=True, upload_to='', verbose_name='画像2')),
                ('image3', models.ImageField(blank=True, upload_to='', verbose_name='画像3')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='作成日時')),
                ('updated_at', models.DateTimeField(auto_now=True, verbose_name='更新日時')),
                ('match_user', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='match_posts', to=settings.AUTH_USER_MODEL, verbose_name='マッチングユーザー')),
                ('user', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='posts', to=settings.AUTH_USER_MODEL, verbose_name='投稿者名')),
            ],
        ),
        migrations.CreateModel(
            name='Message',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('content', models.TextField(verbose_name='本文')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='作成日時')),
                ('user', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='会員名')),
                ('post', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='GOODstime.post', verbose_name='投稿名')),
            ],
        ),
        migrations.CreateModel(
            name='Favorite',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='作成日時')),
                ('updated_at', models.DateTimeField(auto_now=True, verbose_name='更新日時')),
                ('user', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='会員名')),
                ('post', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='GOODstime.post', verbose_name='投稿名')),
            ],
        ),
        migrations.CreateModel(
            name='Comment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('content', models.TextField(verbose_name='本文')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='作成日時')),
                ('user', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='会員名')),
                ('post', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='GOODstime.post', verbose_name='投稿名')),
            ],
        ),
        migrations.CreateModel(
            name='Report',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('comment', models.TextField(blank=True, verbose_name='内容')),
                ('delete_flg', models.BooleanField(default=False, verbose_name='削除フラグ')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='作成日時')),
                ('updated_at', models.DateTimeField(auto_now=True, verbose_name='更新日時')),
                ('post', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='GOODstime.post', verbose_name='投稿名')),
                ('user', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='会員名')),
            ],
        ),
        migrations.CreateModel(
            name='Review',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('score', models.PositiveIntegerField(choices=[(1, '良かった'), (2, '悪かった')], verbose_name='評価')),
                ('comment', models.TextField(blank=True, verbose_name='コメント')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='作成日時')),
                ('target_user', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='target_reviews', to=settings.AUTH_USER_MODEL, verbose_name='対象会員名')),
                ('user', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='reviews', to=settings.AUTH_USER_MODEL, verbose_name='会員名')),
            ],
        ),
        migrations.CreateModel(
            name='Stripe_Customer',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('stripeCustomerId', models.CharField(max_length=255, verbose_name='カスタマーID')),
                ('stripeSubscriptionId', models.CharField(blank=True, max_length=255, null=True, verbose_name='サブスクリプションID')),
                ('stripePaymentMethodId', models.CharField(blank=True, max_length=255, null=True, verbose_name='支払い方法')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='作成日時')),
                ('updated_at', models.DateTimeField(auto_now=True, verbose_name='更新日時')),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='stripe_customer', to=settings.AUTH_USER_MODEL, verbose_name='会員名')),
            ],
        ),
    ]