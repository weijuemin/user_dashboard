# -*- coding: utf-8 -*-
# Generated by Django 1.9.7 on 2016-07-25 00:15
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user_dashboard', '0002_message_targetuser'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='description',
            field=models.TextField(default='None'),
        ),
    ]
