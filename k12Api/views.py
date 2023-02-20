from django.shortcuts import render, redirect
from django.http import HttpResponse
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.exceptions import AuthenticationFailed
from .Serializer import TrainerDetailSerializer, TrainingSerializer, schoolDetailSerializer, userSerializer
from .models import TrainerDetails, TrainingDetails, schoolDetail
from .models import Users
import jwt, datetime

# Create your views here.


def Home(request):
    return HttpResponse("I'm Home")


############################################ Post and Get Request Function for Trainer #########################################################

@api_view(['POST', 'GET'])
def TrainerDetail(request):
    if request.method == 'POST':
        serTrainerData = TrainerDetailSerializer(data=request.data)
        if serTrainerData.is_valid():
            serTrainerData.save()
        else:
            return Response({'Error': serTrainerData.errors})
        return Response(serTrainerData.data)

    if request.method == 'GET':
        trainerData = TrainerDetails.objects.all()
        serializeTrainingData = TrainerDetailSerializer(trainerData, many=True)
        return Response(serializeTrainingData.data)

########################################### GET, PUT, DELETE Request based on ID #############################################################

@api_view(['PUT', 'DELETE', 'GET'])
def TrainerOperation(request, id):
    try:
        trainerObj = TrainerDetails.objects.get(pk=id)
    except:
        return Response({'status': 404})
    if request.method == 'DELETE':
        trainerObj.delete()
        return Response({"status": "Data Deleted"})

    elif request.method == 'PUT':
        serializedata = TrainerDetailSerializer(trainerObj, data=request.data)
        if serializedata.is_valid():
            serializedata.save()
            return Response(serializedata.data)
        return Response({'status': 404})

    elif request.method == 'GET':
        serializedData = TrainerDetailSerializer(trainerObj)
        return Response(serializedData.data)


############################################ Post and Get Request Function for Training #########################################################

@api_view(['POST', 'GET'])
def TrainingDetail(request):
    if request.method == 'POST':
        try:
            serTraining = TrainingSerializer(data=request.data)
            if serTraining.is_valid():
                serTraining.save()
            else:
                return Response(serTraining.errors)
            return Response(serTraining.data)
        except Exception as e:
            return Response(e)

    if request.method == 'GET':
        trainingsObj = TrainingDetails.objects.all()
        serializeTraining = TrainingSerializer(trainingsObj, many=True)
        return Response(serializeTraining.data)


############################################ Post and Get Request Function for School #########################################################

@api_view(['POST', 'GET'])
def schoolData(request):
    if request.method == 'POST':
        serSchoolData = schoolDetailSerializer(data=request.data)
        if serSchoolData.is_valid():
            serSchoolData.save()
        else:
            return Response({'Error': serSchoolData.errors})
        return Response(serSchoolData.data)

    if request.method == 'GET':
        schoolObj = schoolDetail.objects.all()
        serializedSchool = schoolDetailSerializer(schoolObj, many=True)
        return Response(serializedSchool.data)


############################################ GET, DELETE and PUT based on ID #########################################################

@api_view(['GET', 'PUT', 'DELETE'])
def schoolDataOperations(request, id):
    try:
        schoolObj = schoolDetail.objects.get(pk=id)
    except:
        return Response(status="Not Found")

    if request.method == 'GET':
        serializedData = schoolDetailSerializer(schoolObj)
        return Response(serializedData.data)

    elif request.method == 'PUT':
        serialized = schoolDetailSerializer(schoolObj, data=request.data)
        if serialized.is_valid():
            serialized.save()
            return Response(serialized.data)
        return Response(serialized.errors, status='HTTP_400_BAD_REQUEST')
    elif request.method == 'DELETE':
        schoolObj.delete()
        return Response({'Message': 'Data has been deleted'})


########################################## For User Register ######################################################

@api_view(['POST'])
def userRegister(request):
    user = userSerializer(data=request.data)
    if user.is_valid():
        user.save()
    else:
        return Response(user.errors)
    return Response(user.data)
    

###################################### For user Authentication and Login #################################
@api_view(['POST','GET'])
def userLogin(request):
    if request.method == 'POST':
        email = request.data['email']
        password = request.data['password']

        user = Users.objects.filter(email=email).first()
        if user is None:
            raise AuthenticationFailed("User not Found")
        
        if not user.check_password(password):
            raise AuthenticationFailed("Incorrect password")
        
        payload = {
            'id' : user.id,
            'exp' : datetime.datetime.utcnow() + datetime.timedelta(minutes=60),
            'iat' : datetime.datetime.utcnow()
        }

        token = jwt.encode(payload, 'secret', algorithm='HS256')
        response = Response()
        response.set_cookie(key='jwt', value=token, httponly=True)
        response.data = {
            'token':token
        }
        return response

    elif request.method == 'GET':
        token = request.COOKIES.get('jwt')
        if not token:
            raise AuthenticationFailed('No Token found')
        
        try:
            payload = jwt.decode(token, 'secret', algorithms=['HS256'])
        except jwt.ExpiredSignatureError:
            raise AuthenticationFailed('Unauthenticated')
        
        user = Users.objects.filter(id=payload['id']).first()
        userData = userSerializer(user)
        return Response(userData.data)

################################ Handelling Logout #####################################
@api_view(['POST'])
def logOut(request):
    response = Response()
    response.delete_cookie('jwt')
    response.data = {
        'status':"Logout"
    }
    return response
