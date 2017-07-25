# -*- coding: utf-8 -*-
# Generated by Django 1.11.3 on 2017-07-25 03:19
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0007_auto_20170725_0315'),
    ]

    operations = [
        migrations.AddField(
            model_name='studentprofile',
            name='home_address',
            field=models.CharField(default='Cau Giay,Ha Noi,Viet Nam', max_length=256),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='studentprofile',
            name='joined_time',
            field=models.DateField(auto_now=True),
        ),
    ]
