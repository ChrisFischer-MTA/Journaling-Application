from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse
from .models import JournalEntry

# Create your views here.

def journals(request):
    journal_entries = JournalEntry.objects.all()
    return render(request, 'journalindex.html', {'journal_entries': journal_entries}) #HttpResponse("Hello world!")

def journal_detail(request, id):
    entry = get_object_or_404(JournalEntry, id=id)
    return render(request, 'journal_detail.html', {'entry': entry})
