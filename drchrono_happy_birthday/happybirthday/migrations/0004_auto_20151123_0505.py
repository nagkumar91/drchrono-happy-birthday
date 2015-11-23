# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('happybirthday', '0003_auto_20151120_0208'),
    ]

    operations = [
        migrations.RenameField(
            model_name='accesstoken',
            old_name='token',
            new_name='patient_token',
        ),
        migrations.AddField(
            model_name='accesstoken',
            name='user_token',
            field=models.CharField(default='hello', max_length=255),
            preserve_default=False,
        ),
    ]
