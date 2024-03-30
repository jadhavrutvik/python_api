from rest_framework.decorators import api_view,permission_classes,authentication_classes
from rest_framework.response import Response
from rest_framework.authentication import BasicAuthentication
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework_simplejwt.views import TokenObtainPairView
import io
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
        stream=io.BytesIO(json_data)
        python_data=JSONParser().parse(stream)
        with open(path,'r') as f:
            exiting_data=json.load(f)

        exiting_data['items'].append(python_data)
        with open(path, 'w') as f:
            json.dump(exiting_data,f, indent=4)
        return Response('Data posted!')
    
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