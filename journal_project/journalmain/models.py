from django.db import models
from django.contrib.auth.models import User

# Blurbs are messages sent throughout the day when
# things happen that remind you to journal about the topic.
class Blurbs(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    journalEntry = models.ForeignKey('JournalEntry', on_delete=models.CASCADE, null=True, blank=True)
    blurb_text = models.CharField(max_length=256, blank=True, null=True)


# Create your models here.
class JournalEntry(models.Model):
    # The user who made the journal entry
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    # The date the journal entry was made
    date = models.DateField(auto_now_add=True)

    # The title of the journal entry
    title = models.CharField(max_length=1024, blank=True, null=True)

    # The content of the journal entry
    content = models.TextField(blank=True, null=True)

    # The mood or emotions associated with the journal entry
    mood = models.CharField(max_length=50, blank=True, null=True)

    # Any goals or tasks associated with the journal entry
    goals = models.TextField(blank=True, null=True)

    # Any reflections or insights from the journal entry
    reflections = models.TextField(blank=True, null=True)

    # Any gratitude or positive thoughts from the journal entry
    gratitude = models.TextField(blank=True, null=True)

    # The time the journal entry was made
    created_at = models.DateTimeField(auto_now=True)

    # The time the journal entry was last updated
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.user.username}'s Journal Entry for {self.date}"

    class Meta:
        verbose_name_plural = "Journal Entries"
