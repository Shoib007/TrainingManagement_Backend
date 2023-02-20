from django.contrib import admin
from .models import TrainerDetails, TrainingDetails, schoolDetail, Users

# Register your models here.
admin.site.register([TrainerDetails, TrainingDetails, schoolDetail, Users])