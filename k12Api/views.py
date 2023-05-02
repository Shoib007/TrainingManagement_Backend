import os
from django.shortcuts import render, redirect
from django.contrib.auth.hashers import make_password
from django.http import HttpResponse
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from rest_framework.exceptions import AuthenticationFailed
from .Serializer import TrainerDetailSerializer, TrainingSerializer, schoolDetailSerializer, userSerializer
from .models import TrainerDetails, TrainingDetails, schoolDetail
from .models import Users
import jwt, datetime


def Home(request):
    return HttpResponse("I'm Home")


############################################ Post and Get Request Function for Trainer #########################################################

@api_view(['POST', 'GET'])
def TrainerDetail(request):
    if request.method == 'POST':
        data = request.data
        hashPass = make_password(data['email'])
        ######### Creating User ###########
        user = Users.objects.create(
            name = data['fname'],
            email = data['email'],
            password = hashPass,
            phoneNumber = data['contact'],
        )
        ######### Saving Trainer data ##########
        trainer = TrainerDetails.objects.create(
            user = user,
            fname = data['fname'],
            contact = data['contact'],
            trainerLink = data['trainerLink'],
            email = data['email'],
            trainer_type = data['trainer_type'],
            department = data['department'],
        )
        return Response({"status":200})
    
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

########################### Updating Training's State ####################################


@api_view(['PUT','GET'])
def trainingUpdate(request, tID):
    if request.method == 'PUT':
        training = TrainingDetails.objects.get(id=tID)
        schoolID = training.schoolName.id                   # Getting school ID of this training
        school = schoolDetail.objects.get(id= schoolID)     # getting that particular school data based on id

        if len(request.data) > 3:
            updateTraining = TrainingSerializer(training, data=request.data)
            if updateTraining.is_valid():
                return Response("Training Updated")
            return Response(updateTraining.errors)
        else:
            training.state = request.data['state']
            school.state = request.data['state']
            print("Training Updated")
        training.save()
        school.save()
        
        return Response("State updated")
    if request.method == 'GET':
        training = TrainingDetails.objects.get(id=tID)
        serTraining = TrainingSerializer(training)
        data = serTraining.data
        data['trainerName'] = training.trainerName.fname
        data['TrainingDate'] = training.TrainingDate.strftime('%m/%d/%Y')
        return Response(serTraining.data)




############################## Specific Training Data ##########################################

@api_view(["GET"])
def trainerTrainingData(request, trainer_id):
    training = TrainingDetails.objects.filter(trainerName__user_id= trainer_id)
    serTraining = TrainingSerializer(training, many=True)
    return Response(serTraining.data)


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


############################################ School GET, DELETE and PUT based on ID #########################################################

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
    

###################################### For user Authentication and Register and Login #################################
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
        userData = userSerializer(user, context={'request':request})
        return Response(userData.data)

@api_view(['PUT'])
def updateUser(request, userId):
    userData = Users.objects.get(id=userId)
    try:
        if 'profile' in request.FILES:
            # first delete old image
            old_profile_path = userData.profile.path
            if os.path.exists(old_profile_path):
                os.remove(old_profile_path)

            #set new image now
            userData.profile = request.FILES['profile']
            print(userData.profile.path)
            userData.save()
            return Response("No issue")
        else:
            return Response("No image found")
    except Exception as e:
        return Response({"error":str(e)})
    
   

################################ Handelling Logout #####################################
@api_view(['POST'])
def logOut(request):
    response = Response()
    response.delete_cookie('jwt')
    response.data = {
        'status':"Logout"
    }
    return response