# Generated by Django 5.1.7 on 2025-05-29 14:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Alibaba', '0016_alter_order_payment_option'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='status',
            field=models.CharField(choices=[('Draft', 'Draft'), ('Pending', 'Pending'), ('Confirmed', 'Confirmed'), ('Processing', 'Processing'), ('Shipped', 'Shipped'), ('Delivered', 'Delivered'), ('Cancelled', 'Cancelled'), ('Failed', 'Failed')], default='Pending', max_length=233),
        ),
    ]
