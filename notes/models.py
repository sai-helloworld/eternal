# Create your models here.
from django.db import models

class Note(models.Model):
    subject = models.CharField(max_length=100)
    unit = models.CharField(max_length=50)
    title = models.CharField(max_length=200)
    file = models.FileField(upload_to="notes/")
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.subject} - {self.unit} - {self.title}"
