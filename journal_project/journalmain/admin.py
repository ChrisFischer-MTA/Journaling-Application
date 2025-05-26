from django.contrib import admin
from .models import JournalEntry, Blurb, Report

# Register your models here.
admin.site.register(JournalEntry)
admin.site.register(Blurb)
admin.site.register(Report)
