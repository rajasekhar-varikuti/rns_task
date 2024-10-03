from django.db import models

# Create your models here.

class FileData(models.Model):
    file_name = models.CharField(max_length=255)
    file_key = models.CharField(max_length=255)
    #Either s3_url or file_location is sufficient to  save file
    s3_url = models.URLField(null=True, blank=True)
    file_location = models.FileField()
    uploaded_at = models.DateTimeField(auto_now_add=True)