from django.urls import path
from .views import *

urlpatterns = [
    path('', Home, name='Home'),
    path('trainerdata', TrainerDetail, name='TrainerDetail'),
    path('trainerdata/<int:id>', TrainerOperation, name='TrainerOperation'),
    path('training', TrainingDetail, name='TrainingDetail'),
    path('schooldata', schoolData, name='schoolData'),
    path('schooldata/<int:id>', schoolDataOperations, name='schoolData'),
    path('register',userRegister, name='userRegister'),
    path('login',userLogin,name='userLogin'),
    path('logout', logOut, name='logOut'),
]