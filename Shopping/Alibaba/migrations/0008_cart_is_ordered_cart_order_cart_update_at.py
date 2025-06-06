# Generated by Django 5.1.7 on 2025-05-16 18:15

import django.db.models.deletion
import django.utils.timezone
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Alibaba', '0007_order_status'),
    ]

    operations = [
        migrations.AddField(
            model_name='cart',
            name='is_ordered',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='cart',
            name='order',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='Alibaba.order'),
        ),
        migrations.AddField(
            model_name='cart',
            name='update_at',
            field=models.DateTimeField(default=django.utils.timezone.now),
        ),
    ]
