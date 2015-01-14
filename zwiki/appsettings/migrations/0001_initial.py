# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Setting',
            fields=[
                ('id', models.AutoField(verbose_name='ID', auto_created=True, serialize=False, primary_key=True)),
                ('title', models.CharField(max_length=255)),
                ('slug', models.CharField(max_length=255, unique=True)),
                ('value', models.CharField(max_length=500)),
            ],
            options={
                'abstract': False,
            },
            bases=(models.Model,),
        ),
    ]
