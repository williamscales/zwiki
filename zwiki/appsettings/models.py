from django.db import models

from zwiki.sluggable.models import Sluggable

class Setting(Sluggable):
    value = models.CharField(max_length=500)

    def __str__(self):
        return self.title
