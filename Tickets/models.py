from django.db import models


# Create your models here.
class Ticket(models.Model):
    assignee_id = models.IntegerField()
    created_at = models.DateTimeField(null=True, blank=True)
    description = models.CharField(max_length=200)
    due_at = models.DateTimeField(null=True, blank=True)
    has_incidents = models.BooleanField(null=True)
    id = models.IntegerField(primary_key=True)
    priority = models.CharField(null=True, max_length=200)
    problem_id = models.IntegerField(null=True)
    raw_subject = models.CharField(null=True, max_length=200)
    recipient = models.EmailField(null=True)
    requester_id = models.IntegerField(null=True)
    satisfaction_rating = models.JSONField(null=True)
    status = models.CharField(null=True, max_length=200)
    subject = models.CharField(null=True, max_length=200)
    submitter_id = models.IntegerField(null=True)
    tags = models.JSONField(null=True, blank=True)
    type = models.CharField(null=True, max_length=200)
    updated_at = models.DateTimeField(null=True)
    url = models.URLField(null=True)

    def __str__(self):
        return str(self.id) + " " + str(self.updated_at) + " " + str(self.description)
