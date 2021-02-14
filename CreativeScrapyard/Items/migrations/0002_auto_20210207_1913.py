# Generated by Django 3.1.4 on 2021-02-07 13:43

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Items', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='tbl_creativeitems_details',
            name='crt_item_details_id',
            field=models.AutoField(primary_key=True, serialize=False, validators=[django.core.validators.MaxValueValidator(9999999999)]),
        ),
        migrations.AlterField(
            model_name='tbl_creativeitems_mst',
            name='crt_item_id',
            field=models.AutoField(primary_key=True, serialize=False, validators=[django.core.validators.MaxValueValidator(9999999999)]),
        ),
        migrations.AlterField(
            model_name='tbl_crtimages',
            name='crt_img_id',
            field=models.AutoField(primary_key=True, serialize=False, validators=[django.core.validators.MaxValueValidator(99999)]),
        ),
    ]
