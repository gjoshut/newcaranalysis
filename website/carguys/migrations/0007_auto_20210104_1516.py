# Generated by Django 3.1.4 on 2021-01-04 21:16

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('carguys', '0006_auto_20201231_1230'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='presale',
            options={'ordering': ('Model',)},
        ),
    ]