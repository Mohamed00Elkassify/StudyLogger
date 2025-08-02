from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
# Create your models here.
class Session(models.Model):
    subject = models.CharField(max_length=255)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    duration = models.PositiveBigIntegerField(help_text="Duration in minutes")
    date = models.DateField()
    created_at = models.DateTimeField(default=timezone.now)


    def __str__(self):
        return f"{self.subject} - {self.duration_human} on {self.date}"

    @property
    def duration_human(self):
        hours = self.duration // 60
        minutes = self.duration % 60
        return f"{hours}h {minutes}m" if hours else f"{minutes}m"
