from django.contrib import admin
from .models import JournalEntry, Blurb

# Register your models here.
admin.site.register(JournalEntry)
admin.site.register(Blurb)
