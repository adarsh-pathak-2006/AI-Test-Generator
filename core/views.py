from django.shortcuts import render, get_object_or_404
from core.serializer import *
from core.models import *
from rest_framework.views import APIView
from rest_framework.response import Response
from services.output import final_output
from rest_framework.generics import RetrieveUpdateAPIView


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
            output_data=final_output(doc=document)
            main_obj=MainDB.objects.create(user=request.user, document=document)
            for output in output_data:
                quesans_serial=QuesAnsSerializer(data=output)
                if quesans_serial.is_valid():
                    question=quesans_serial.validated_data['question']
                    option1=quesans_serial.validated_data['option1']
                    option2=quesans_serial.validated_data['option2']
                    option3=quesans_serial.validated_data['option3']
                    option4=quesans_serial.validated_data['option4']
                    correct_ans=quesans_serial.validated_data['correct_ans']
                    Quesans.objects.create(main=main_obj, question=question, option1=option1, option2=option2, option3=option3, option4=option4, correct_ans=correct_ans)
                else:
                    return Response({ 'invalid':'invalid ai response returned' })
        else:
            return Response({ 'invalid':'invalid inputs' })        


class QuizAPI(APIView):
    def get(self, request, pk, ck):
        main_obj=get_object_or_404(MainDB, user=request.user, id=pk)
        ques_data=get_object_or_404(Quesans, input=main_obj, id=ck)
        serial=QuestionSerializer(ques_data)
        return Response(serial.data)
    
    def put(self, request, pk, ck):
        main_obj=get_object_or_404(MainDB, user=request.user, id=pk)
        ques_data=get_object_or_404(Quesans, main=main_obj, id=ck)
        serial=AnswerSerializer(ques_data, data=request.data)
        if serial.is_valid():
            answer=serial.validated_data['answer']
            if answer==ques_data.correct_ans:
                ques_data.mark=1
                ques_data.save()
                return Response({ 'message':'correct answer' })
            else:
                return Response({ 'message':'wrong answer' })
        else:
            return Response({ 'message':'invalid input' })
        

    