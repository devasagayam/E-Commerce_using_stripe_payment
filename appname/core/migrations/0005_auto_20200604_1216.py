# Generated by Django 3.0.5 on 2020-06-04 06:46

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0004_orderitem_ordered_date'),
    ]

    operations = [
        migrations.RenameField(
            model_name='orderitem',
            old_name='ordered_date',
            new_name='due_date',
        ),
    ]
