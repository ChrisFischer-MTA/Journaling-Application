from django.shortcuts import render
from django.http import HttpResponse
from .models import JournalEntry

# Create your views here.

def journals(request):
    journal_entries = JournalEntry.objects.all()
    return render(request, 'journalindex.html', {'journal_entries': journal_entries}) #HttpResponse("Hello world!")
