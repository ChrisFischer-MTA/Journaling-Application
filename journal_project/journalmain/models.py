from django.db import models
from django.contrib.auth.models import User

# Blurbs are messages sent throughout the day when
# things happen that remind you to journal about the topic.
class Blurbs(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    journalEntry = models.ForeignKey('JournalEntry', on_delete=models.CASCADE, null=True, blank=True)
    blurb_text = models.CharField(max_length=256, blank=True, null=True)

class Goal(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    goal_title = models.CharField(max_length=256, blank=False, null=False)
    goal_text = models.CharField(max_length=1024, blank=False, null=False)
    goal_rationale = models.CharField(max_length=1024, blank=False, null=False)
    goalCreated = models.DateTimeField(auto_now=True)
    journals = models.ManyToManyField('JournalEntry')
    LENGTH_CHOICES = [
        ('1m', '1 Month'),
        ('6m', '6 Months'),
        ('1y', '1 Year'),
        ('5y', '5 Years'),
    ]
    length = models.CharField(
        max_length=2,
        choices=LENGTH_CHOICES,
        default='1m',  # Set a default value if needed
    )

# Create your models here.
class JournalEntry(models.Model):
    # The user who made the journal entry
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    date = models.DateField(auto_now_add=True)
    title = models.CharField(max_length=1024, blank=True, null=True)
    content = models.TextField(blank=True, null=True)
    mood = models.CharField(max_length=128, blank=True, null=True)
    reflections = models.TextField(blank=True, null=True)
    gratitude = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.user.username}'s Journal Entry for {self.date}"

    class Meta:
        verbose_name_plural = "Journal Entries"
