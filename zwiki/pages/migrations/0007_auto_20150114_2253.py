# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('pages', '0006_auto_20150114_2019'),
    ]

    operations = [
        migrations.AlterField(
            model_name='pagehistory',
            name='categories',
            field=models.ManyToManyField(to='pages.Category', blank=True, null=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='pagehistory',
            name='page',
            field=models.ForeignKey(related_name='page_history', to='pages.Page'),
            preserve_default=True,
        ),
    ]
