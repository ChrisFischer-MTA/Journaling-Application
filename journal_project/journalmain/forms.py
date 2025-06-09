from django import forms

from .models import JournalEntry


class JournalForm(forms.ModelForm):
    class Meta:
        model = JournalEntry
        fields = ["content", "reflections", "gratitude"]


class AskJournalForm(forms.Form):
    def __init__(self, *args, **kwargs):
        self.user = kwargs.get("user")
        kwargs.pop("user")
        # This is unhinged.
        super().__init__(*args, **kwargs)
        self.fields["journals"].queryset = JournalEntry.objects.filter(user=self.user)

    question = forms.CharField(widget=forms.Textarea, max_length=125)
    journals = forms.ModelMultipleChoiceField(
        queryset=JournalEntry.objects.all(),
        widget=forms.SelectMultiple(attrs={"size": "40"}),
    )

    class Meta:
        fields = ["user", "question", "journals"]
