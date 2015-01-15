# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('pages', '0004_page_lock_time'),
    ]

    operations = [
        migrations.AddField(
            model_name='page',
            name='html',
            field=models.TextField(default='<p>Regenerate the HTML for this page by editing it and then saving it</p>'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='pagehistory',
            name='html',
            field=models.TextField(default='No HTML for this page.'),
            preserve_default=False,
        ),
    ]
