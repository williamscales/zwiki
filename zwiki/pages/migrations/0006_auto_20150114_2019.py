# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('pages', '0005_auto_20150114_1918'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='pagehistory',
            name='slug',
        ),
        migrations.AlterField(
            model_name='pagehistory',
            name='title',
            field=models.TextField(max_length=255),
            preserve_default=True,
        ),
    ]
