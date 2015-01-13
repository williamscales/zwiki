# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('pages', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='category',
            name='slug',
            field=models.CharField(max_length=255, default='foo'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='page',
            name='slug',
            field=models.CharField(max_length=255, default='foo'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='pagehistory',
            name='slug',
            field=models.CharField(max_length=255, default='foo'),
            preserve_default=False,
        ),
    ]
