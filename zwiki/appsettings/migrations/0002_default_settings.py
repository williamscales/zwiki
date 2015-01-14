# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


def default_settings(apps, schema_editor):
    Setting = apps.get_model('appsettings', 'Setting')

    default_settings = [
        Setting(title='Site Name', slug='site-name', value='ZWiki'),
        Setting(title='Site Webmaster Email', slug='site-webmaster-email',
                value='zwiki@example.com'),
    ]
    for setting in default_settings:
        setting.save()


class Migration(migrations.Migration):

    dependencies = [
        ('appsettings', '0001_initial'),
    ]

    operations = [
        migrations.RunPython(default_settings),
    ]
