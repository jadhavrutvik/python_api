from grpc import Status
from rest_framework.decorators import api_view,permission_classes,authentication_classes
from rest_framework.response import Response
from rest_framework.authentication import BasicAuthentication
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework_simplejwt.views import TokenObtainPairView
import io
from django.views.decorators.csrf import csrf_exempt
from django.middleware.csrf import get_token
from rest_framework import status
from django.contrib.auth import authenticate
from django.shortcuts import render,redirect
from rest_framework.parsers import JSONParser
from myproject.settings import BASE_DIR
path=f"{BASE_DIR}\\myapp\\data.json"
import json
from rest_framework.permissions import IsAuthenticated
from myapp.serializers  import *


@api_view(['GET'])
@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated])
def get_data(request,id):
    if request.method == 'GET':
        with open(path,'r') as f:
            data = json.load(f)
            d=data['items'][int(id)]
        return Response(d)


@api_view(['GET'])
@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated])
def get_all_data(request):
    if request.method == 'GET':
        with open(path,'r') as f:
            data = json.load(f)
        return Response(data)


@api_view(["POST"])
@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated])
def post_data(request):
    if request.method=="POST":
        json_data=request.body
        print(json_data)
        stream=io.BytesIO(json_data)
        python_data=JSONParser().parse(stream)
        if  all(key in python_data for key in ["id","name","designation"]):
            with open(path,'r') as f:
                exiting_data=json.load(f)

            exiting_data['items'].append(python_data)
            with open(path, 'w') as f:
                json.dump(exiting_data,f, indent=4)
            return Response("Data posted successfully!", status=status.HTTP_201_CREATED)
        else:
            return Response("Please provide 'id', 'name', and 'designation' in the request.", status=status.HTTP_400_BAD_REQUEST)


     
@api_view(["DELETE"])
@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated])
def delete_data(request,id):
    if request.method=="DELETE":
        with open(path,'r') as f:
            data=json.load(f)
            del data["items"][int(id)]
        with open(path, 'w') as f:
            json.dump(data,f, indent=4)
        return Response("Item deleted!")



class MyTokenObtainPairView(TokenObtainPairView):
    serializer_class = MyTokenObtainPairSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        return Response(serializer.validated_data)


@api_view(['GET'])
@csrf_exempt  # Exempt this view from CSRF protection for testing
def get_csrf_token(request):
    csrf_token = get_token(request)
    return Response({"csrf_token": csrf_token})