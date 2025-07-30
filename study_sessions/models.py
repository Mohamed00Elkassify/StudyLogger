from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Sessions(models.Model):
    subject = models.CharField(max_length=255)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    duration = models.DurationField()
    date = models.DateField()
    notes = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)


    def __str__(self):
        return f"{self.subject} - {self.duration} min on {self.date}"

