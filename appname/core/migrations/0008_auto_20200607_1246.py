# Generated by Django 3.0.5 on 2020-06-07 07:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0007_remove_order_due_date'),
    ]

    operations = [
        migrations.AddField(
            model_name='orderitem',
            name='action',
            field=models.BooleanField(default=False),
        ),
        migrations.AlterField(
            model_name='item',
            name='category',
            field=models.CharField(choices=[('S', 'Costume'), ('OW', 'Party Time Products')], max_length=2),
        ),
    ]
