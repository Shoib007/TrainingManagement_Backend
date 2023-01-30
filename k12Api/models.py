from django.db import models

# Create your models here.
class TrainerDetails(models.Model):
    trainerName = models.CharField(max_length=255)
    trainerLink = models.URLField(max_length=255)
    doj = models.DateField()
    trainer_type = models.CharField(max_length=200)
    department = models.CharField(max_length=200)