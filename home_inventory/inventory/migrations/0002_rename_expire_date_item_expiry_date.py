# Generated by Django 4.0 on 2021-12-29 09:12

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('inventory', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='item',
            old_name='expire_date',
            new_name='expiry_date',
        ),
    ]