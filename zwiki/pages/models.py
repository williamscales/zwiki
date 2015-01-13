from django.db import models
from django.contrib.auth.models import User


class Page(models.Model):
    title = models.CharField(max_length=255)
    slug = models.CharField(max_length=255)
    date_published = models.DateTimeField(auto_now_add=True)
    edit_summary = models.TextField()
    content = models.TextField()
    public = models.BooleanField(default=False)
    author = models.ForeignKey(User)
    categories = models.ManyToManyField('Category', related_name='pages',
                                        null=True, blank=True)

    def __str__(self):
        return self.title

    class Meta:
        ordering = ('date_published',)
        permissions = (
            ('view_page', 'Can see existance of page and page contents'),
        )


class PageHistory(models.Model):
    title = models.CharField(max_length=255)
    slug = models.CharField(max_length=255)
    date_published = models.DateTimeField(auto_now_add=True)
    edit_summary = models.TextField()
    content = models.TextField()
    public = models.BooleanField(default=False)
    author = models.ForeignKey(User)
    page = models.ForeignKey(Page)
    categories = models.ManyToManyField('Category',
                                        related_name='page_histories',
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


class Category(models.Model):
    title = models.CharField(max_length=255)
    slug = models.CharField(max_length=255)
    description = models.TextField()
    parent = models.ForeignKey('self', related_name='categories', null=True,
                               blank=True)

    def __str__(self):
        return self.title

    class Meta:
        ordering = ('title',)
        verbose_name_plural = 'categories'
