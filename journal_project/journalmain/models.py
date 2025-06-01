from django.db import models
from django.contrib.auth.models import User

# Blurbs are messages sent throughout the day when
# things happen that remind you to journal about the topic.
class Blurb(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    journalEntry = models.ForeignKey('JournalEntry', on_delete=models.CASCADE, null=True, blank=True)
    blurb_text = models.CharField(max_length=256)
    created_at = models.DateTimeField(auto_now=True)
    updated_at = models.DateTimeField(auto_now=True)


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
    parent_goal = models.ForeignKey("self", on_delete=models.CASCADE)

class Report(models.Model):
    # The user field exists so we know who "owns" the report, and
    # from that we can determine who can view it
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=1024)
    TYPE_CHOICES = [
        ('w', '1 Week'),
        ('m', '1 Month'),
        ('6', '6 Months'), # note that anything beyond this is not implemented yet
        ('y', '1 Year'),   # and may not be implemented until I find a model that can fit it
    ]
    type = models.CharField(
        max_length=1,
        choices=TYPE_CHOICES,
        default='w',  # Set a default value if needed
    )
    content = models.TextField()

    def __str__(self):
        return self.title


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
    week_report = models.ForeignKey(Report, on_delete=models.CASCADE, related_name='week_report', blank=True, null=True)
    month_report = models.ForeignKey(Report, on_delete=models.CASCADE, related_name='month_report', blank=True, null=True)

    def __str__(self):
        return f"{self.user.username}'s Journal Entry for {self.date}"

    class Meta:
        verbose_name_plural = "Journal Entries"
