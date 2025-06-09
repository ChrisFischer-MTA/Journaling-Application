from django.contrib import admin

from .models import Blurb, JournalEntry, Report

# Register your models here.
admin.site.register(JournalEntry)
admin.site.register(Blurb)
admin.site.register(Report)
