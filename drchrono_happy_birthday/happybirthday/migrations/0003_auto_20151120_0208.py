# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('happybirthday', '0002_auto_20151120_0203'),
    ]

    operations = [
        migrations.AddField(
            model_name='accesstoken',
            name='refresh_token',
            field=models.CharField(default='aaa', max_length=255),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='accesstoken',
            name='doctor',
            field=models.ForeignKey(related_name='access_tokens', blank=True, to=settings.AUTH_USER_MODEL, null=True),
        ),
    ]
