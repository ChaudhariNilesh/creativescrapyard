# Generated by Django 3.1.5 on 2021-01-31 14:16

import django.core.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('Items', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='tbl_orders_mst',
            fields=[
                ('order_id', models.PositiveIntegerField(primary_key=True, serialize=False, validators=[django.core.validators.MaxValueValidator(9999999999)])),
                ('person_name', models.CharField(max_length=20)),
                ('contact_no', models.CharField(max_length=10)),
                ('delivery_address', models.CharField(max_length=350)),
                ('total_amt', models.DecimalField(decimal_places=2, max_digits=15, validators=[django.core.validators.MinValueValidator(0)])),
                ('order_date', models.DateTimeField(auto_now_add=True)),
                ('delivery_status', models.CharField(choices=[('PENDING', 'Pending'), ('DISPATCHED', 'Dispatched'), ('DELIVERED', 'Delivered'), ('CANCELLED', 'Cancelled')], max_length=15)),
                ('delivery_date', models.DateTimeField(auto_now_add=True)),
            ],
        ),
        migrations.CreateModel(
            name='tbl_orders_details',
            fields=[
                ('order_details_id', models.PositiveIntegerField(primary_key=True, serialize=False, validators=[django.core.validators.MaxValueValidator(9999999999)])),
                ('crt_item_qty', models.PositiveIntegerField(default=1, validators=[django.core.validators.MaxValueValidator(999)])),
                ('unit_price', models.DecimalField(decimal_places=2, max_digits=15, validators=[django.core.validators.MinValueValidator(0)])),
                ('pickup_address', models.CharField(max_length=350)),
                ('item_status', models.CharField(choices=[('PLACED', 'Placed'), ('COMPLETED', 'Completed'), ('CANCELLED', 'Cancelled'), ('FAILED', 'Failed'), ('RETURNED', 'Returned')], max_length=15)),
                ('crt_item_details', models.ForeignKey(null=True, on_delete=django.db.models.deletion.RESTRICT, to='Items.tbl_creativeitems_details')),
                ('order', models.ForeignKey(on_delete=django.db.models.deletion.RESTRICT, to='Order.tbl_orders_mst')),
            ],
        ),
    ]
