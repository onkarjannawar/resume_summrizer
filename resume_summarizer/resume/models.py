from django.db import models

# Create your models here.
class myuploadfile(models.Model):
    myfiles=models.FileField(upload_to="")
