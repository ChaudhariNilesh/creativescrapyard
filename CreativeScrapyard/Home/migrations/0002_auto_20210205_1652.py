# Generated by Django 3.1.4 on 2021-02-05 11:22

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Home', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='query',
            name='first_name',
            field=models.CharField(max_length=100),
        ),
        migrations.AlterField(
            model_name='query',
            name='last_name',
            field=models.CharField(max_length=100),
        ),
        migrations.AlterField(
            model_name='query',
            name='query_id',
            field=models.AutoField(primary_key=True, serialize=False, validators=[django.core.validators.MaxValueValidator(9999999999)]),
        ),
    ]