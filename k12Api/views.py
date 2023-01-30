from django.shortcuts import render, redirect
from django.http import HttpResponse
from rest_framework.decorators import api_view
from rest_framework.response import Response
# from .models import TrainerDetails
from .Serializer import TrainerDetailSerializer

# Create your views here.

def Home(request):
    return HttpResponse("I'm Home")

@api_view(['POST'])
def TrainerDetail(request):
    serTrainerData = TrainerDetailSerializer(data= request.data)
    if serTrainerData.is_valid():
        serTrainerData.save()
    else:
        return Response({'Error': serTrainerData.errors})
    return redirect('/')