import requests
import os

mood_prompt = """You're an AI who is unbiased and is tasked with analyzing a journal/diary entry below. You've been given the following mood list, in python3 list format, to use as possible outputs (important! you may ONLY output elements in the list). You're tasked with reading the journal entry and pulling out moods from it. Your output should be a list of moods, no more then 7 moods. It can be as short as possible. If it's impossible to pull out any moods at all (this should be unlikely!), you will output an empty python list. In all cases, the outputted list should be a valid python list.\n\n```python3\nmoods = [\n    'happy',\n    'sad',\n    'angry',\n    'afraid',\n    'excited',\n    'calm',\n    'worried',\n    'in love',\n    'surprised',\n    'proud',\n    'ashamed',\n    'frustrated',\n    'guilty',\n    'curious',\n    'nostalgic',\n    'hopeful',\n    'disappointed',\n    'embarrassed',\n    'envious',\n    'grateful',\n    'longing',\n    'relieved',\n    'optimistic',\n    'pessimistic'\n]\n```\n\nJournal Entry: \n"""
title_prompt = """You're an AI who is unbiased and is tasked with analyzing a journal/diary entry below. You've been given the following task: Generate a short (important! less then 100 characters) title that describes a main topic of the journal. The title should be something that reminds the author of what they wrote about if they saw a list of titles. Your output, after thinking, should just be the title with no formatting.\nJournal Entry: \n"""

def process_entry(entry, tries):
    if tries > 5:
        print("Five tries exceeded!")
        return
    response = requests.post('http://ollama-intel-gpu:11434/api/generate', json={'model':'deepseek-r1:14b','stream':False,'prompt':mood_prompt+f'```\n{entry.content}\n```'})
    if "python3" not in str(response.json()):
        return process_entry(entry, tries+1)
    moods = response.json()['response'].split('```')[1].replace('python3','').replace('\n','')
    entry.mood = moods
    response = requests.post('http://ollama-intel-gpu:11434/api/generate', json={'model':'deepseek-r1:14b','stream':False,'prompt':title_prompt+f'```\n{entry.content}\n```'})
    entry.title = response.json()['response'].split('</think>')[1].strip().replace('*', '').replace('"','').replace('Title:', '').replace('Title','').strip()
    entry.save()


os.environ.setdefault("DJANGO_SETTINGS_MODULE", "journal_project.settings")
from django.core.wsgi import get_wsgi_application
get_wsgi_application()
from journalmain.models import Blurb, JournalEntry
from django.contrib.auth.models import User


journalEntries = JournalEntry.objects.filter(title=None)
for entry in journalEntries:
    process_entry(entry, 0)
