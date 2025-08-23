# Create your models here.
from django.db import models


class ClassNote(models.Model):
    class_id = models.CharField(max_length=20)  # e.g., "CSE101", "MATH202"
    subject_name = models.CharField(max_length=100)  # e.g., "Data Structures"
    pdf_file = models.FileField(upload_to='notes_pdfs/')  # stored in MEDIA_ROOT/notes_pdfs/
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.subject_name} - {self.class_id}"
