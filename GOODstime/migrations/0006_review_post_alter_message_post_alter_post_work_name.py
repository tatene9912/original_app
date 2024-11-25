# Generated by Django 5.1.3 on 2024-11-24 13:39

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('GOODstime', '0005_alter_post_status_alter_post_work_name'),
    ]

    operations = [
        migrations.AddField(
            model_name='review',
            name='post',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='GOODstime.post', verbose_name='投稿名'),
        ),
        migrations.AlterField(
            model_name='message',
            name='post',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='messages', to='GOODstime.post', verbose_name='投稿名'),
        ),
        migrations.AlterField(
            model_name='post',
            name='work_name',
            field=models.CharField(max_length=100, verbose_name='投稿名'),
        ),
    ]
