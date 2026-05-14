from django.urls import path
from . import views

app_name = 'qna'

urlpatterns = [
    path('', views.index, name='index'),
    path('questions/<int:id>', views.question_detail, name='question_detail'),
    path('answer/create/<int:id>', views.answer_create, name='answer_create'),
    path('answer/delete/<int:answer_id>', views.answer_delete, name='answer_delete'),

    path('question/create', views.question_create, name='question_create'),
    path('question/modify/<int:id>', views.question_modify, name='question_modify'),
    path('question/delete/<int:id>', views.question_delete, name='question_delete'),

    path('question/vote/<int:id>', views.question_vote, name='question_vote'),
    path('answer/vote/<int:id>', views.answer_vote, name='answer_vote'),
]