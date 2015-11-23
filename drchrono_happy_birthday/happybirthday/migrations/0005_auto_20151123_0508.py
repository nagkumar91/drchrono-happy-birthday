# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('happybirthday', '0004_auto_20151123_0505'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='accesstoken',
            name='client_id',
        ),
        migrations.RemoveField(
            model_name='accesstoken',
            name='client_secret',
        ),
        migrations.RemoveField(
            model_name='accesstoken',
            name='refresh_token',
        ),
        migrations.RemoveField(
            model_name='accesstoken',
            name='scope',
        ),
    ]
