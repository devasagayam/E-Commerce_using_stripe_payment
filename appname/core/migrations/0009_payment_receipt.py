# Generated by Django 3.0.5 on 2020-06-08 07:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0008_auto_20200607_1246'),
    ]

    operations = [
        migrations.AddField(
            model_name='payment',
            name='receipt',
            field=models.BooleanField(default=0),
        ),
    ]
