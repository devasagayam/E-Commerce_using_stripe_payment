# Generated by Django 3.0.5 on 2020-06-22 10:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0009_payment_receipt'),
    ]

    operations = [
        migrations.AddField(
            model_name='refund',
            name='trid',
            field=models.CharField(blank=True, max_length=21),
        ),
    ]
