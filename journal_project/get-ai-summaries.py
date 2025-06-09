import datetime
import os

import requests

mood_prompt = """You're an AI who is unbiased and is tasked with analyzing a journal/diary entry below. You've been given the following mood list, in python3 list format, to use as possible outputs (important! you may ONLY output elements in the list). You're tasked with reading the journal entry and pulling out moods from it. Your output should be a list of moods, no more then 7 moods. It can be as short as possible. If it's impossible to pull out any moods at all (this should be unlikely!), you will output an empty python list. In all cases, the outputted list should be a valid python list.\n\n```python3\nmoods = [\n    'happy',\n    'sad',\n    'angry',\n    'afraid',\n    'excited',\n    'calm',\n    'worried',\n    'in love',\n    'surprised',\n    'proud',\n    'ashamed',\n    'frustrated',\n    'guilty',\n    'curious',\n    'nostalgic',\n    'hopeful',\n    'disappointed',\n    'embarrassed',\n    'envious',\n    'grateful',\n    'longing',\n    'relieved',\n    'optimistic',\n    'pessimistic'\n]\n```\n\nJournal Entry: \n"""
title_prompt = """You're an AI who is unbiased and is tasked with analyzing a journal/diary entry below. You've been given the following task: Generate a short (important! less then 100 characters) title that describes a main topic of the journal. The title should be something that reminds the author of what they wrote about if they saw a list of titles. Your output, after thinking, should just be the title with no formatting.\nJournal Entry: \n"""
summary_prompt="You're an AI who is unbiased and is tasked with analyzing a week's worth of journal/diary entry below. You've been given the goal of creating a high level summary of trends in this week's journals. Your analysis should include information such as the common topics that were covered across journals and sentiment analysis about those topics. If the author of the journals seemed unhappy about something and it ended up working out, put a brief positive note about that. After the conclusion of all of that analysis, you're to provide recommendations on future lines of effort the author can do (important! only output recommendations if they're not immediately obvious and are relevant. It is better to have no such recommendations then generic or unhelpful ones). "

def process_entry(entry, tries):
    if tries > 5:
        print("Five tries exceeded!")
        return None
    response = requests.post('http://ollama-intel-gpu:11434/api/generate', json={'model':'deepseek-r1:14b','stream':False,'prompt':mood_prompt+f'```\n{entry.content}\n```'})
    if "python3" not in str(response.json()):
        return process_entry(entry, tries+1)
    moods = response.json()['response'].split('```')[1].replace('python3','').replace('\n','')
    entry.mood = moods
    response = requests.post('http://ollama-intel-gpu:11434/api/generate', json={'model':'deepseek-r1:14b','stream':False,'prompt':title_prompt+f'```\n{entry.content}\n```'})
    entry.title = response.json()['response'].split('</think>')[1].strip().replace('*', '').replace('"','').replace('Title:', '').replace('Title','').strip()
    entry.save()
    return None


os.environ.setdefault("DJANGO_SETTINGS_MODULE", "journal_project.settings")
from django.core.wsgi import get_wsgi_application

get_wsgi_application()
from journalmain.models import JournalEntry, Report

# Process individual entries for Titles and Summaries.
journalEntries = JournalEntry.objects.filter(title=None)
for entry in journalEntries:
    process_entry(entry, 0)

# Search for eligible journals for weekly reports. Decompose queryset to list 
# for iteration. Use order by to ensure the "earliest" journals come first.
journalEntries = list(JournalEntry.objects.filter(week_report=None).order_by('date'))
# Handly little trick I know - we can use the ISO week number and year as a key
# for a dictionary then iterate through the dictionary
to_process = {} # XXX: This needs to be renamed from to_process to journal_entries_dictionary
for entry in journalEntries:
    entry_key = str(entry.date.isocalendar()[0:2]) + f'_USER_{entry.user.id!s}'
    # If it's this CURRENT week, it's not due for processing.
    if entry_key == str(datetime.datetime.now().isocalendar()[0:2]) + f'_USER_{entry.user.id!s}':
        continue
    if to_process.get(entry_key) is None:
        to_process[entry_key] = []
    to_process[entry_key].append(entry)

for key, journal_entry in to_process.items():
    journals = to_process[key]
    # Create a text blob to store the journals
    blob = ""
    for i in range(len(journals)):
        last_journal_date = journal_entry.date.isocalendar()[0:2]
        blob += f"\nJournal {i}:\n```\n{journal_entry.content}\n```"
    response = requests.post('http://ollama-intel-gpu:11434/api/generate', json={'model':'deepseek-r1:14b','stream':False,'prompt':summary_prompt+f'```\n{blob}\n```'})
    report_obj = Report(user=journals[0].user, type='w', title=f'Week {last_journal_date!s} Journal Report', content=response.json()['response'].split('</think>')[1].strip())
    report_obj.save()
    for entry in journals:
        entry.week_report = report_obj
        entry.save()
