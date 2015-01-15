import base64
from datetime import datetime, timedelta, timezone
import json

from docutils.core import publish_string

from django.db import models
from django.contrib.auth.models import User

from zwiki.sluggable.models import Sluggable


class Page(Sluggable):
    """A page in the wiki"""

    UNLOCKED = 'UU'
    LOCKED = 'LL'
    LOCK_STATE_CHOICES = (
        (UNLOCKED, 'Unlocked'),
        (LOCKED, 'Locked'),
    )

    lock_state = models.CharField(max_length=2, choices=LOCK_STATE_CHOICES,
                                  default=UNLOCKED)
    lock_time = models.DateTimeField(null=True, blank=True)
    lock_owner = models.ForeignKey(User, null=True, blank=True,
                                   related_name='locks')
    date_published = models.DateTimeField(auto_now_add=True)
    edit_summary = models.TextField()
    content = models.TextField()
    html = models.TextField()
    public = models.BooleanField(default=False)
    author = models.ForeignKey(User)
    categories = models.ManyToManyField('Category', related_name='pages',
                                        null=True, blank=True)

    def __str__(self):
        return self.title

    def lock(self, user):
        self.lock_state = self.LOCKED
        self.lock_time = datetime.now()
        self.lock_owner = user
        self.save()

    def unlock(self):
        self.lock_state = self.UNLOCKED
        self.lock_time = None
        self.lock_owner = None
        self.save()

    def save(self, *args, **kwargs):
        # Process the user-inputted RST when we save
        self.generate_rst()
        super(Page, self).save(*args, **kwargs)

    def generate_rst(self):
        """Convenience function to render RST from Page.content into Page.html

        """
        defaults = {
            'file_insertion_enabled': 0,
            'raw_enabled': 0,
            '_disable_config': 1,
        }
        self.html = publish_string(self.content,
                                   writer_name='html',
                                   settings_overrides=defaults)
        return self.html

    def lock_is_fresh(self):
        if datetime.now(timezone.utc) <= self.lock_time + timedelta(hours=2):
            return True
        else:
            return False

    class Meta:
        ordering = ('date_published',)
        permissions = (
            ('view_page', 'Can see existance of page and page contents'),
        )


class PageHistory(models.Model):
    """A specific past revision of a page in the wiki."""
    title = models.TextField(max_length=255)
    date_published = models.DateTimeField(auto_now_add=True)
    edit_summary = models.TextField()
    content = models.TextField()
    html = models.TextField()
    public = models.BooleanField(default=False)
    author = models.ForeignKey(User)
    page = models.ForeignKey(Page, related_name='page_history')
    categories = models.ManyToManyField('Category',
                                        null=True, blank=True)

    def __str__(self):
        return 'revision of "{}" from {}'.format(self.title,
                                                 self.date_published)

    class Meta:
        ordering = ('title', 'date_published',)
        permissions = (
            ('view_page_history', 'Can see page history'),
        )
        verbose_name_plural = 'page history objects'


class Category(Sluggable):
    """A named grouping of wiki pages and possibly sub-categories"""
    description = models.TextField()
    parent = models.ForeignKey('self', related_name='categories', null=True,
                               blank=True)

    def __str__(self):
        return self.title

    class Meta:
        ordering = ('title',)
        verbose_name_plural = 'categories'
