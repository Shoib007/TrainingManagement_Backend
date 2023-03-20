from django.urls import path
from .views import *
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    path('', Home, name='Home'),
    path('trainerdata', TrainerDetail, name='TrainerDetail'),
    path('trainerdata/<int:id>', TrainerOperation, name='TrainerOperation'),
    path('training', TrainingDetail, name='TrainingDetail'),
    path('login/<int:userId>', updateUser, name="updateUser"),
    # path('Trainertraining/<int:userId>', updateTraining, name="updateTraining"),
    path('schooldata', schoolData, name='schoolData'),
    path('schooldata/<int:id>', schoolDataOperations, name='schoolData'),
    path('login',userLogin,name='userLogin'),
    path('logout', logOut, name='logOut'),
    path('training/<int:trainer_id>', trainerTrainingData, name="trainerTrainingData"),
    path('trainingUpdate/<int:tID>', trainingUpdate, name='trainingUpdate')
]

urlpatterns += static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)