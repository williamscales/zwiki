# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('pages', '0003_page_lock_owner'),
    ]

    operations = [
        migrations.AddField(
            model_name='page',
            name='lock_time',
            field=models.DateTimeField(null=True, blank=True),
            preserve_default=True,
        ),
    ]
