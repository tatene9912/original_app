# Generated by Django 5.1.3 on 2024-11-22 12:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('GOODstime', '0003_alter_comment_post'),
    ]

    operations = [
        migrations.AddField(
            model_name='post',
            name='status',
            field=models.CharField(blank=True, max_length=20, null=True, verbose_name='ステータス'),
        ),
    ]
