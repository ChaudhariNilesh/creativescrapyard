# Generated by Django 3.1.4 on 2021-02-18 12:20

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Items', '0006_auto_20210218_1622'),
    ]

    operations = [
        migrations.RenameField(
            model_name='issues',
            old_name='crt_item_id',
            new_name='crt_item',
        ),
        migrations.RenameField(
            model_name='issues',
            old_name='scp_item_id',
            new_name='scp_item',
        ),
    ]
