#from django.forms import ModelForm, TextField, ModelMultipleChoiceField, SelectMultiple
from django import forms
from django.contrib.auth.models import User
from .models import JournalEntry, Goal


class JournalForm(forms.ModelForm):
    class Meta:
        model = JournalEntry
        fields = ['content', 'reflections', 'gratitude']



class AskJournalForm(forms.Form):
    def __init__(self, *args, **kwargs):
        self.user = kwargs.get('user')
        kwargs.pop('user')
        # This is unhinged.
        super().__init__(*args, **kwargs)
        self.fields['journals'].queryset = JournalEntry.objects.filter(user=self.user)

    question = forms.CharField(widget=forms.Textarea, max_length=960)
    journals = forms.ModelMultipleChoiceField(queryset=JournalEntry.objects.all(), widget=forms.SelectMultiple(attrs={"size": "40"}))

    class Meta:
        fields = ['user', 'question', 'journals'] 

    

class GoalForm(forms.ModelForm):
    class Meta:
        model = Goal
        fields = ('goal_title', 'goal_text', 'goal_rationale', 'length', 'parent_goal')

    def clean(self):
        cleaned_data = super().clean()
        parent_goal = cleaned_data.get('parent_goal')
        if parent_goal and parent_goal == self.instance:
            raise forms.ValidationError("A goal cannot be its own parent")
        return cleaned_data
