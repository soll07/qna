from django.db import models
from django.contrib.auth.models import User   # Django가 만들어 둔 User
from django import forms

class Question(models.Model):
    author = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='questions')
    subject = models.CharField(max_length=200) # 기본값 null=False, blank=False
    content = models.TextField() # 기본값 null=False, blank=False
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)

    voters = models.ManyToManyField(User, related_name='question_votes')

    def __str__(self):
        return f'[{self.id}] {self.subject}'

class Answer(models.Model):
    author = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='authored_answers')
    question = models.ForeignKey(Question, on_delete=models.CASCADE, related_name='answers')
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)

    voters = models.ManyToManyField(User, related_name='answer_votes')

    def __str__(self):
        return f'[{self.id}] Q{self.content}'
    
# ModelForm 상속 = 모델을 그대로 써서 폼을 만들어 주는 단축 클래스
# 1. (Question Model과 관련있는 속성)화면에 보일 라벨 설정 가능
# 2. (Question Model과 관련있는 속성)저장할 수 있는 필드 제공
# 3. (Question Model과 관련있는 속성)유효성 검사(검증)
class QuestionForm(forms.ModelForm):
    class Meta:
        model = Question
        fields = ['subject', 'content']
        labels = {
            'subject': '제목',
            'content': '내용'
        }