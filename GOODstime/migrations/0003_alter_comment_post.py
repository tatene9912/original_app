# Generated by Django 5.1.3 on 2024-11-20 15:40

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('GOODstime', '0002_alter_post_match_user'),
    ]

    operations = [
        migrations.AlterField(
            model_name='comment',
            name='post',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='comments', to='GOODstime.post', verbose_name='投稿名'),
        ),
    ]
