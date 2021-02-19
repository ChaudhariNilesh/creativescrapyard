# Generated by Django 3.1.4 on 2021-02-18 12:32

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('Items', '0008_auto_20210218_1758'),
    ]

    operations = [
        migrations.AlterField(
            model_name='issues',
            name='reported_user',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='reportee', to=settings.AUTH_USER_MODEL),
        ),
    ]
