# Generated by Django 3.1.4 on 2021-03-09 19:10

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('Items', '0007_auto_20210224_0025'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='issues',
            name='crt_item',
        ),
        migrations.AddField(
            model_name='issues',
            name='crt_item_id',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='Items.tbl_creativeitems_mst'),
        ),
        migrations.AlterField(
            model_name='issues',
            name='scp_item',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='Items.tbl_scrapitems'),
        ),
    ]