# Generated by Django 3.1.4 on 2021-03-02 17:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Order', '0003_auto_20210302_2050'),
    ]

    operations = [
        migrations.AlterField(
            model_name='tbl_orders_mst',
            name='order_date',
            field=models.DateTimeField(auto_now=True),
        ),
    ]