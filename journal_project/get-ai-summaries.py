import requests
import os

mood_prompt = """You're an AI who is unbiased and is tasked with analyzing a journal/diary entry below. You've been given the following mood list, in python3 list format, to use as possible outputs (important! you may ONLY output elements in >
title_prompt = """You're an AI who is unbiased and is tasked with analyzing a journal/diary entry below. You've been given the following task: Generate a short (important! less then 100 characters) title that describes a main topic of the jou>


def process_entry(entry, tries):
    if tries > 5:
        print("Five tries exceeded!")
        return
    response = requests.post('http://ollama-intel-gpu:11434/api/generate', json={'model':'deepseek-r1:14b','stream':False,'prompt':mood_prompt+f'```\n{entry.content}\n```'})
    if "python3" not in response.content:
        return process_entry(entry, tries+1)
    moods = response.json()['response'].split('```')[1].replace('python3','').replace('\n','')
    entry.mood = moods
    response = requests.post('http://ollama-intel-gpu:11434/api/generate', json={'model':'deepseek-r1:14b','stream':False,'prompt':title_prompt+f'```\n{entry.content}\n```'})
    entry.title = response.json()['response'].split('</think>')[1].strip().replace('*', '').replace('"','')
    entry.save()


os.environ.setdefault("DJANGO_SETTINGS_MODULE", "journal_project.settings")
from django.core.wsgi import get_wsgi_application
get_wsgi_application()
from journalmain.models import Blurb, JournalEntry
from django.contrib.auth.models import User


journalEntries = JournalEntry.objects.filter(title=None)
for entry in journalEntries:
    process_entry(entry, 0)
