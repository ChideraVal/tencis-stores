# Generated by Django 4.2.16 on 2024-11-04 23:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shopapp', '0009_order_create_time'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='transaction_id',
            field=models.CharField(max_length=150, null=True),
        ),
    ]
