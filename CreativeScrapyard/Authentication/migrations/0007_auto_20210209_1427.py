# Generated by Django 3.1.4 on 2021-02-09 08:57

import Authentication.models
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Authentication', '0006_auto_20210209_1032'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='user_image',
            field=models.ImageField(default='users/default.png', null=True, upload_to=Authentication.models.user_photo),
        ),
        migrations.AlterField(
            model_name='profile',
            name='user_rating',
            field=models.DecimalField(blank=True, decimal_places=1, max_digits=2, null=True),
        ),
    ]
