import os
from django.db import models
from django.contrib.auth.models import AbstractUser
from .manager import UserManager
from django.contrib.postgres.fields import ArrayField

#In this way you can store the profile picture arrange as per the user name folder.
def picturePath(instance, filename):
    return os.path.join('profile',str(instance.name), filename)


############################# User's Table ########################################
class Users(AbstractUser):
    name = models.CharField(max_length=255)
    email = models.CharField(max_length=255, unique=True)
    password = models.CharField(max_length=255)
    phoneNumber = models.BigIntegerField(default=91, null=True)
    profile = models.ImageField(upload_to=picturePath, null=True, blank=True)
    username = None
    objects = UserManager()
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

############################# Trainer's Table ##################################
class TrainerDetails(models.Model):
    user = models.OneToOneField(Users, on_delete=models.CASCADE, primary_key=True)
    fname = models.CharField(max_length=255, default=None)
    contact = models.BigIntegerField(default=91)
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
    # grades = ArrayField(models.CharField(max_length=512, blank=True), blank=True, null=True)

############################# Training's Table ####################################
class TrainingDetails(models.Model):
    trainerName = models.ForeignKey(TrainerDetails, on_delete=models.PROTECT,related_name="TrainerDetails")
    schoolName = models.ForeignKey(schoolDetail, on_delete=models.PROTECT, related_name="SchoolDetails")
    subject = models.CharField(max_length=255, null=True, blank=True)
    startTime = models.TimeField()
    endTime = models.TimeField()
    TrainingDate = models.DateField()
    state = models.CharField(max_length=20, default="pending")
    def __str__(self):
        return f"{self.TrainingDate}"