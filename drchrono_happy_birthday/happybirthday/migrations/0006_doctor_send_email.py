# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('happybirthday', '0005_auto_20151123_0508'),
    ]

    operations = [
        migrations.AddField(
            model_name='doctor',
            name='send_email',
            field=models.BooleanField(default=True),
        ),
    ]
