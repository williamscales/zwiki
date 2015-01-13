# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.AutoField(primary_key=True, verbose_name='ID', serialize=False, auto_created=True)),
                ('title', models.CharField(max_length=255)),
                ('description', models.TextField()),
                ('parent', models.ForeignKey(null=True, to='pages.Category', blank=True, related_name='categories')),
            ],
            options={
                'ordering': ('title',),
                'verbose_name_plural': 'categories',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Page',
            fields=[
                ('id', models.AutoField(primary_key=True, verbose_name='ID', serialize=False, auto_created=True)),
                ('title', models.CharField(max_length=255)),
                ('date_published', models.DateTimeField(auto_now_add=True)),
                ('edit_summary', models.TextField()),
                ('content', models.TextField()),
                ('public', models.BooleanField(default=False)),
                ('author', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
                ('categories', models.ManyToManyField(to='pages.Category', blank=True, related_name='pages', null=True)),
            ],
            options={
                'ordering': ('date_published',),
                'permissions': (('view_page', 'Can see existance of page and page contents'),),
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='PageHistory',
            fields=[
                ('id', models.AutoField(primary_key=True, verbose_name='ID', serialize=False, auto_created=True)),
                ('title', models.CharField(max_length=255)),
                ('date_published', models.DateTimeField(auto_now_add=True)),
                ('edit_summary', models.TextField()),
                ('content', models.TextField()),
                ('public', models.BooleanField(default=False)),
                ('author', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
                ('categories', models.ManyToManyField(to='pages.Category', blank=True, related_name='page_histories', null=True)),
                ('page', models.ForeignKey(to='pages.Page')),
            ],
            options={
                'ordering': ('title', 'date_published'),
                'permissions': (('view_page_history', 'Can see page history'),),
                'verbose_name_plural': 'page history objects',
            },
            bases=(models.Model,),
        ),
    ]
