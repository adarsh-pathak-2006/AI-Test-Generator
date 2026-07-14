from django.urls import path
from core.views import *

urlpatterns = [
    path('dashboard/', DashboardAPI.as_view(), name='dashboard'),
    path('quiz/<int:pk>/<int:ck>/', QuizAPI.as_view(), name='quiz'),
]
