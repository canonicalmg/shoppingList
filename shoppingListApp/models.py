from __future__ import unicode_literals
from django.contrib.auth.models import User
from django.db import models
from django.template.defaultfilters import slugify
from django.core.validators import RegexValidator

# Create your models here.
# class listType(models.Model):
#     name = models.CharField(max_length=300)
#
#     def __unicode__(self):
#         return self.name

class profile(models.Model):
    phone_regex = RegexValidator(regex=r'^\+?1?\d{9,15}$', message="Phone number must be entered in the format: '+999999999'. Up to 15 digits allowed.")
    number = models.CharField(validators=[phone_regex], blank=True, max_length=15)
    user = models.ForeignKey(User)

class list(models.Model):
    listName = models.CharField(max_length=300)
    slug = models.SlugField()
    owner = models.ForeignKey(profile)

    def save(self, *args, **kwargs):
        if self.slug is None:
            self.slug = slugify(self.listName)
        super(list, self).save(*args, **kwargs)

    def __unicode__(self):
        return self.owner.user.username + " - " + self.listName

class listEntry(models.Model):
    listActual = models.ForeignKey(list)
    itemName = models.CharField(max_length=50)
    shopName = models.CharField(max_length=50)
    quantity = models.CharField(max_length=10)
    price = models.CharField(max_length=10)

    def __unicode__(self):
        return self.itemName + " - " + self.listActual.listName + " - " + self.listActual.owner.user.username