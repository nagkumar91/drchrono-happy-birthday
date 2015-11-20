# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('happybirthday', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='AccessToken',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('client_id', models.CharField(max_length=255)),
                ('client_secret', models.CharField(max_length=255)),
                ('scope', models.CharField(max_length=255)),
                ('token', models.CharField(max_length=255)),
            ],
        ),
        migrations.AlterModelOptions(
            name='doctor',
            options={'verbose_name': 'Doctor', 'verbose_name_plural': 'Doctors'},
        ),
        migrations.AddField(
            model_name='accesstoken',
            name='doctor',
            field=models.ForeignKey(related_name='access_tokens', to=settings.AUTH_USER_MODEL),
        ),
    ]
