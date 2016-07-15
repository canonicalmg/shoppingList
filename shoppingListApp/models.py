from __future__ import unicode_literals
from django.contrib.auth.models import User
from django.db import models
from django.template.defaultfilters import slugify

# Create your models here.
# class listType(models.Model):
#     name = models.CharField(max_length=300)
#
#     def __unicode__(self):
#         return self.name

class list(models.Model):
    listName = models.CharField(max_length=300)
    slug = models.CharField(max_length=300)
    owner = models.ForeignKey(User)

    def save(self, *args, **kwargs):
        if self.slug is None:
            self.slug = slugify(self.listName)
        super(list, self).save(*args, **kwargs)

    def __unicode__(self):
        return self.owner.username + " - " + self.listName

class listEntry(models.Model):
    listActual = models.ForeignKey(list)
    itemName = models.CharField(max_length=50)
    shopName = models.CharField(max_length=50)
    quantity = models.CharField(max_length=10)
    price = models.CharField(max_length=10)

    def __unicode__(self):
        return self.itemName + " - " + self.listActual.listName + " - " + self.listActual.owner.username