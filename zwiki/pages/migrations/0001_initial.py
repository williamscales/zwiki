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
                ('id', models.AutoField(verbose_name='ID', auto_created=True, serialize=False, primary_key=True)),
                ('title', models.CharField(max_length=255)),
                ('slug', models.CharField(max_length=255, unique=True)),
                ('description', models.TextField()),
                ('parent', models.ForeignKey(null=True, blank=True, to='pages.Category', related_name='categories')),
            ],
            options={
                'verbose_name_plural': 'categories',
                'ordering': ('title',),
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Page',
            fields=[
                ('id', models.AutoField(verbose_name='ID', auto_created=True, serialize=False, primary_key=True)),
                ('title', models.CharField(max_length=255)),
                ('slug', models.CharField(max_length=255, unique=True)),
                ('date_published', models.DateTimeField(auto_now_add=True)),
                ('edit_summary', models.TextField()),
                ('content', models.TextField()),
                ('public', models.BooleanField(default=False)),
                ('author', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
                ('categories', models.ManyToManyField(to='pages.Category', related_name='pages', null=True, blank=True)),
            ],
            options={
                'permissions': (('view_page', 'Can see existance of page and page contents'),),
                'ordering': ('date_published',),
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='PageHistory',
            fields=[
                ('id', models.AutoField(verbose_name='ID', auto_created=True, serialize=False, primary_key=True)),
                ('title', models.CharField(max_length=255)),
                ('slug', models.CharField(max_length=255, unique=True)),
                ('date_published', models.DateTimeField(auto_now_add=True)),
                ('edit_summary', models.TextField()),
                ('content', models.TextField()),
                ('public', models.BooleanField(default=False)),
                ('author', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
                ('categories', models.ManyToManyField(to='pages.Category', related_name='page_histories', null=True, blank=True)),
                ('page', models.ForeignKey(to='pages.Page')),
            ],
            options={
                'permissions': (('view_page_history', 'Can see page history'),),
                'verbose_name_plural': 'page history objects',
                'ordering': ('title', 'date_published'),
            },
            bases=(models.Model,),
        ),
    ]
