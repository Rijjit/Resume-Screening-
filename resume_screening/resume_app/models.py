# from django.db import models

# Create your models here.
from django.db import models

class Resume(models.Model):
    file = models.FileField(upload_to='resumes/')
    uploaded_at = models.DateTimeField(auto_now_add=True)
    extracted_text = models.TextField(blank=True)
    score = models.FloatField(default=0.0)  # Match percentage