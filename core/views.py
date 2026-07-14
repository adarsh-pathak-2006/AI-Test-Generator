from django.shortcuts import render, get_object_or_404
from core.serializer import *
from core.models import *
from rest_framework.views import APIView
from rest_framework.response import Response
from services.output import final_output
from core.throttle import LoginUserThrottle, RegisterUserThrottle, QuizCreationThrottle
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework.permissions import IsAuthenticated
import json


class CustomObtainPair(TokenObtainPairView):
    throttle_classes=[LoginUserThrottle]

class RegisterAPI(APIView):
    throttle_classes=[RegisterUserThrottle]
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
    permission_classes=[IsAuthenticated]
    def get_throttles(self):
        if self.request.method=='POST':
            return [QuizCreationThrottle()]
        return [] 

    def get(self, request):
        data=MainDB.objects.filter(user=request.user).order_by('-created_at')
        serial=DashboardQuizSerializer(data, many=True)
        return Response(serial.data)

    def post(self , request):
        serial=MainDBSerializer(data=request.data)
        if serial.is_valid():
            document=serial.validated_data['document']
            output_data_str=final_output(doc=document)
            try:
                # Remove any markdown formatting the AI might add
                cleaned_output = output_data_str.strip()
                if cleaned_output.startswith("```json"):
                    cleaned_output = cleaned_output[7:]
                if cleaned_output.endswith("```"):
                    cleaned_output = cleaned_output[:-3]
                output_data = json.loads(cleaned_output)
            except json.JSONDecodeError:
                return Response({ 'invalid': 'Failed to parse AI output as JSON' })
                
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
            return Response({ 'message':'Quiz created Successfully', 'quiz_id': main_obj.id }) 
        else:
            return Response({ 'invalid':'invalid inputs' })        


class QuizAPI(APIView):
    permission_classes=[IsAuthenticated]
    def get(self, request, pk, ck):
        main_obj=get_object_or_404(MainDB, user=request.user, id=pk)
        ques_data=get_object_or_404(Quesans, main=main_obj, id=ck)
        serial=QuestionSerializer(ques_data)
        return Response(serial.data)
    
    def put(self, request, pk, ck):
        main_obj=get_object_or_404(MainDB, user=request.user, id=pk)
        ques_data=get_object_or_404(Quesans, main=main_obj, id=ck)
        serial=AnswerSerializer(ques_data, data=request.data)
        if serial.is_valid():
            answer=serial.validated_data['answer']
            if answer==ques_data.correct_ans:
                ques_data.mark='R'
                ques_data.save()
                main_obj.score+=1
                main_obj.save(user=request.user)
                return Response({ 'message':'correct answer' })
            else:
                return Response({ 'message':'wrong answer' })
        else:
            return Response({ 'message':'invalid input' })
        

    