from django.db import models
from django.template.defaultfilters import slugify


class Sluggable(models.Model):
    """Abstract base model class which gives a title and an auto-generated slug
    (a lowercased version of the title with spaces replaced by dashes).

    """
    title = models.CharField(max_length=255)
    slug = models.CharField(max_length=255, unique=True)

    def save(self, *args, **kwargs):
        self.slug = slugify(self.title)
        super(Sluggable, self).save(*args, **kwargs)

    class Meta:
        abstract = True
