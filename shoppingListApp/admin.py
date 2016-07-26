from django.contrib import admin
from .models import list, listEntry, profile,textMessage
# Register your models here.

admin.site.register(list)
admin.site.register(listEntry)
admin.site.register(profile)
admin.site.register(textMessage)