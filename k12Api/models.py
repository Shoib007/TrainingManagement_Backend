from django.db import models
from django.contrib.auth.models import AbstractUser
from .manager import UserManager

############################# Trainer's Table ##################################
class TrainerDetails(models.Model):
    fname = models.CharField(max_length=255, default=None)
    # lname = models.CharField(max_length=255, default=None)
    contact = models.IntegerField(default=91)
    trainerLink = models.URLField(max_length=255)
    email = models.EmailField(max_length=255, default='example@example.com')
    trainer_type = models.CharField(max_length=200)
    department = models.CharField(max_length=200)


############################ School' Table #######################################
class schoolDetail(models.Model):
    school = models.CharField(max_length=255)
    region = models.CharField(max_length=255)
    am = models.CharField(max_length=255)
    om = models.CharField(max_length=255)
    catagory = models.CharField(max_length=255)


############################# Training's Table ####################################
class TrainingDetails(models.Model):
    trainerName = models.ForeignKey(TrainerDetails, on_delete=models.PROTECT,related_name="TrainerDetails")
    schoolName = models.ForeignKey(schoolDetail, on_delete=models.PROTECT, related_name="SchoolDetails")
    startTime = models.TimeField()
    endTime = models.TimeField()
    TrainingDate = models.DateField()


############################# User's Table ########################################
class Users(AbstractUser):
    name = models.CharField(max_length=255)
    email = models.CharField(max_length=255, unique=True)
    password = models.CharField(max_length=255)
    phoneNumber = models.IntegerField(default=91, null=True)
    username = None
    objects = UserManager()
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []