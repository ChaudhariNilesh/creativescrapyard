# Generated by Django 3.1.4 on 2021-03-11 16:48

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('Items', '0011_auto_20210311_2217'),
    ]

    operations = [
        migrations.AddField(
            model_name='tbl_scrapitems',
            name='username',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='buyer_username', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='tbl_scrapitems',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.RESTRICT, related_name='seller_id', to=settings.AUTH_USER_MODEL),
        ),
    ]
