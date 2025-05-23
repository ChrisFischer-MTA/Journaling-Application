from django.forms import ModelForm
from .models import JournalEntry

class JournalForm(ModelForm):
    class Meta:
        model = JournalEntry
        fields = ['content', 'reflections', 'gratitude']
