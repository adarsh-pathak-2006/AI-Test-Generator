from django.shortcuts import render, get_object_or_404
from core.serializer import *
from core.models import *
from rest_framework.views import APIView
from rest_framework.response import Response
from services.output import final_output


class RegisterAPI(APIView):
    def post(self, request):
        serial=RegisterSerializer(data=request.data)
        if serial.is_valid():
            f_name=serial.validated_data['first_name']
            l_name=serial.validated_data['last_name']
            username=serial.validated_data['username']
            email=serial.validated_data['email']
            password=serial.validated_data['password']

            if User.objects.filter(username=username).exists():
                return Response({ 'message':'user already exists' })
            else:
                User.objects.create_user(first_name=f_name, last_name=l_name, username=username, email=email, password=password)
                return Response({ 'message':'User Registration Successfull' })
        else:
            return Response({ 'invalid':'invalid inputs' }) 


class DashboardAPI(APIView):
    def get(self, request):
        data=MainDB.objects.filter(user=request.user)
        serial=MainDBSerializer(data, many=True)
        return Response(serial.data)

    def post(self , request):
        serial=MainDBSerializer(data=request.data)
        if serial.is_valid():
            document=serial.validated_data['document']
            serial.save(user=request.user)
            output_data=final_output(input=document)
            for output in output_data:
                quesans_serial=QuesAnsSerializer(data=output)
                if quesans_serial.is_valid():
                    quesans_serial.save(input__user=request.user)
                else:
                    return Response({ 'invalid':'invalid ai response returned' })
        else:
            return Response({ 'invalid':'invalid inputs' })        


