# Generated by Django 3.1.4 on 2021-02-09 23:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Authentication', '0007_auto_20210209_1427'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='bio',
            field=models.TextField(blank=True, default='default', max_length=200, null=True),
        ),
    ]
